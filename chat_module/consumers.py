import json

from ai_profiles.models import BotProfile
from chat_module.levels import calculate_level
from user_profiles.models import UserProfile
from chat_module.models import ChatHistory
from chat_module.tasks import get_response
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.utils import timezone
from django.contrib.auth.models import User


# TODO: When storing bot messages from dialog engine, always store each sentence in a different message line.
# TODO: Make user profile, if user profile is not created
class ChatConsumer(WebsocketConsumer):
    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)

        username = text_data_json["username"]
        bot_id = text_data_json["bot_id"]
        text = text_data_json["text"]
        timestamp = timezone.now().strftime("%Y-%m-%d %H:%M:%S")

        packet = {
            "type": "chat_message",
            # "text": {"msg": text, "source": "user"},
            "who": "user",
            "message": text,
            "username": username,
            "bot_id": bot_id,
            "timestamp": timestamp,
        }

        async_to_sync(self.channel_layer.send)(
            self.channel_name,
            packet,
        )

        user = User.objects.get(username=username)
        user_profile = UserProfile.objects.get(user=user)
        bot = BotProfile.objects.get(bot_id=bot_id)
        chat_history_obj = ChatHistory.objects.get(user=user_profile.user, bot=bot)
        chat_history_obj.history.append(packet)
        characters_sent = sum(1 for c in text if c.isalpha())
        chat_history_obj.input_chars += characters_sent
        user_profile.experience += characters_sent
        chat_history_obj.level = calculate_level(num_chars=chat_history_obj.input_chars)
        chat_history_obj.save()
        user_profile.save()

        get_response(self.channel_name, text_data_json)

    def chat_message(self, event):
        packet = json.dumps(
            {
                "type": "chat_message",
                # "text": event["text"],
                "who": event["who"],
                "message": event["message"],
                "username": event["username"],
                "bot_id": event["bot_id"],
                "timestamp": event["timestamp"],
            }
        )
        self.send(text_data=packet)
