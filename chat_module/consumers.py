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
import logging
from user_profiles.utils import decrypt_email

logger = logging.getLogger("my_logger")


class ChatConsumer(WebsocketConsumer):
    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        logger.info(f"data: {text_data_json}")

        encryption = text_data_json["email"]
        email = decrypt_email(encryption)
        user = User.objects.get(email=email)
        logger.info(f"email: {email}, user: {user}")

        user_profile = UserProfile.objects.get(user=user)

        bot_id = text_data_json["bot_id"]
        bot = BotProfile.objects.get(bot_id=bot_id)

        chat_history_obj = ChatHistory.objects.get(user=user, bot=bot)

        text = text_data_json["text"]

        timestamp = timezone.now().strftime("%Y-%m-%d %H:%M:%S")

        packet = {
            "type": "chat_message",
            "source": "user",
            "who": encryption,
            "message": text,
            "timestamp": timestamp,
        }
        logger.info(f"Packet from user: {packet}")

        async_to_sync(self.channel_layer.send)(
            self.channel_name,
            packet,
        )

        logger.info("Now appending user message to chat history")
        chat_history_obj.history.append({
            "who": packet["who"],
            "message": packet["message"],
            "timestamp": packet["timestamp"]
        })

        characters_sent = sum(1 for c in text if c.isalpha())
        chat_history_obj.input_chars += characters_sent
        user_profile.experience += characters_sent
        chat_history_obj.level = calculate_level(num_chars=chat_history_obj.input_chars)
        chat_history_obj.save()
        user_profile.save()

        get_response(self.channel_name, user, user_profile, bot, chat_history_obj)

    def chat_message(self, event):
        packet = json.dumps(
            {
                "type": "chat_message",
                "source": event["source"],
                "who": event["who"],
                "message": event["message"],
                "timestamp": event["timestamp"],
            }
        )
        logger.info(f"Packet about to be sent: {packet}")
        self.send(text_data=packet)
