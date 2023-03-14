import json

from ai_profiles.models import BotProfile
from .levels import calculate_level
from .models import UserProfile, ChatHistory
from .tasks import get_response
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        get_response.delay(self.channel_name, text_data_json)

        username = text_data_json['username']
        bot_id = text_data_json["bot_id"]
        text = text_data_json["text"]
        packet = {
            "type": "chat_message",
            "text": text,
            "username": username,
            "bot_id": bot_id,
            "timestamp": text_data_json["timestamp"]
        }
        async_to_sync(self.channel_layer.send)(
            self.channel_name,
            packet,
        )

        user_profile = UserProfile.objects.get(username=username)
        bot = BotProfile.objects.get(bot_id=bot_id)
        chat_history_obj = ChatHistory.objects.get(user=user_profile.user, bot=bot)
        chat_history_obj.history.append(packet)
        chat_history_obj.input_chars += sum(1 for c in text if c.isalpha())
        chat_history_obj.save()
        user_profile.level = calculate_level(chat_history_obj.input_chars)
        user_profile.save()

    # NOTE: The structure of 'event' is defined by the UI
    def chat_message(self, event):
        packet = json.dumps({
            "type": "chat_message",
            "text": event["text"],
            "username": event["username"],
            "bot_id": event["bot_id"],
            "timestamp": event["timestamp"]
        })
        self.send(text_data=packet)