import json

from ai_profiles.models import BotProfile
from chat_module.levels import calculate_level
from user_profiles.models import UserProfile
from chat_module.models import ChatHistory
from chat_module.tasks import get_response
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.utils import timezone
from user_profiles.models import User


# TODO: When storing bot messages from dialog engine, always store each sentence in a different message line.
class ChatConsumer(WebsocketConsumer):
    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)

        email = text_data_json["email"]
        bot_id = text_data_json["bot_id"]
        text = text_data_json["text"]
        timestamp = timezone.now().strftime("%Y-%m-%d %H:%M:%S")

        packet = {
            "type": "chat_message",
            # "text": {"msg": text, "source": "user"},
            "source": "user",
            "who": email,
            "message": text,
            "timestamp": timestamp,
        }

        async_to_sync(self.channel_layer.send)(
            self.channel_name,
            packet,
        )

        
        # user = User.objects.first()
        # print(user, User.objects.all())
        
        try:
            user = User.objects.get(email=email)
        except (KeyError, User.DoesNotExist):
            user = User.objects.create(email=email)

        try:
            user_profile = UserProfile.objects.get(user=user)
        except (KeyError, UserProfile.DoesNotExist):
            user_profile = UserProfile.objects.create(user=user)

        bot = BotProfile.objects.get(bot_id=bot_id)

        try:
            chat_history_obj = ChatHistory.objects.get(user=user_profile.user, bot=bot)
        except (KeyError, ChatHistory.DoesNotExist):
            chat_history_obj = ChatHistory.objects.create(
                user=user_profile.user, bot=bot, history=[]
            )

        chat_history_obj.history.append(
            {
                "who": packet["who"],
                "message": packet["message"],
                "timestamp": packet["timestamp"],
            }
        )
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
                "who": event["who"],
                "message": event["message"],
                "source": event["source"],
                "timestamp": event["timestamp"],
            }
        )
        self.send(text_data=packet)
