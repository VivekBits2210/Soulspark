from unittest import skip

from django.test import TestCase
from channels.testing import WebsocketCommunicator
from chat_module.consumers import ChatConsumer
from chat_module.models import UserProfile, ChatHistory
import json
from chat_module.tasks import get_response
from chat_module.tests.utils import create_user_and_profile, create_bot


class ChatConsumerTestCase(TestCase):
    def setUp(self):
        self.user, self.user_profile = create_user_and_profile()
        self.bot = create_bot()
        self.chat_history = ChatHistory.objects.create(
            user=self.user_profile.user, bot=self.bot, history=[], input_chars=0
        )
        self.communication = WebsocketCommunicator(ChatConsumer.as_asgi(), "/ws/chat/")
        self.communication.scope["user"] = self.user_profile.user
        self.communication.scope["url_route"] = {"kwargs": {}}
        self.communication.scope["subprotocols"] = ["test"]

    @skip
    async def test_receive(self):
        message = json.dumps(
            {
                "username": self.user.username,
                "bot_id": self.bot.bot_id,
                "text": "test message",
                "timestamp": "2023-03-14 11:00:00",
            }
        )
        await self.communication.send_json_to({"text": message})
        response = await self.communication.receive_json_from()
        self.assertEqual(response["text"], "test message")

        chat_history_obj = ChatHistory.objects.get(
            user=self.user_profile.user, bot=self.bot
        )
        self.assertEqual(len(chat_history_obj.history), 1)
        self.assertEqual(chat_history_obj.history[0]["username"], self.user.username)
        self.assertEqual(chat_history_obj.history[0]["bot_id"], self.bot.bot_id)
        self.assertEqual(chat_history_obj.history[0]["text"], "test message")
        self.assertEqual(chat_history_obj.input_chars, len("test message"))

    @skip
    async def test_chat_message(self):
        event = {
            "type": "chat_message",
            "text": "test message",
            "username": self.user.username,
            "bot_id": self.bot.bot_id,
            "timestamp": "2023-03-14 11:00:00",
        }
        await self.communication.send_json_to(event)
        response = await self.communication.receive_json_from()
        self.assertEqual(response["text"], "test message")

    @skip
    async def test_communication(self):
        message = json.dumps(
            {
                "username": self.user.username,
                "bot_id": self.bot.bot_id,
                "text": "test message",
                "timestamp": "2023-03-14 11:00:00",
            }
        )
        await self.communication.send_json_to({"text": message})
        response = await self.communication.receive_json_from()
        self.assertEqual(response["text"], "test message")

        event = {
            "type": "chat_message",
            "text": "test response",
            "username": self.user.username,
            "bot_id": self.bot.bot_id,
            "timestamp": "2023-03-14 11:01:00",
        }
        await self.communication.send_json_to(event)
        response = await self.communication.receive_json_from()
        self.assertEqual(response["text"], "test response")

    def tearDown(self):
        self.user.delete()
        self.bot.delete()
        self.chat_history.delete()


class GetResponseTestCase(TestCase):
    def setUp(self):
        self.user, self.user_profile = create_user_and_profile()
        self.bot = create_bot()
        self.chat_history = ChatHistory.objects.create(
            user=self.user_profile.user, bot=self.bot, history=[], input_chars=0
        )

    @skip
    def test_get_response(self):
        channel_name = "test_channel_name"
        input_data = {
            "username": self.user.username,
            "bot_id": self.bot.bot_id,
            "text": "test message",
            "timestamp": "2023-03-14 11:00:00",
        }
        get_response(channel_name, input_data)

        chat_history_obj = ChatHistory.objects.get(user=self.user.user, bot=self.bot)
        self.assertEqual(len(chat_history_obj.history), 1)
        self.assertEqual(chat_history_obj.history[0]["username"], self.user.username)
        self.assertEqual(chat_history_obj.history[0]["bot_id"], self.bot.bot_id)
        self.assertEqual(
            chat_history_obj.history[0]["text"], "This is a canned bot response."
        )

    def tearDown(self):
        self.user.delete()
        self.bot.delete()
        self.chat_history.delete()
