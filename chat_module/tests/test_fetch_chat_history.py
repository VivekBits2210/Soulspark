from django.test import Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from chat_module.models import ChatHistory
from chat_module.tests.utils import create_user_and_profile, create_bot


class FetchChatHistoryTestCase(APITestCase):
    def setUp(self):
        self.url = reverse("fetch_chat_history")
        self.bot = create_bot()
        self.user, self.encrypted_email, self.user_profile = create_user_and_profile()

        self.client = Client()

        self.valid_history = [
            {"message": "hi", "from": "user"},
            {"message": "hey, how can I help", "from": "bot"},
        ]

    def test_fetch_chat_history_works(self):
        # API should work, return a dictionary no bot_id
        response = self.client.get(self.url, data={"email": self.encrypted_email})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_json = response.json()
        self.assertIsInstance(response_json, dict)
        self.assertEqual(response_json["bot_id"], None)
        self.assertEqual(response_json["history"], [])

    def test_fetch_chat_history_with_bot_id_works(self):
        # API should work, return a dictionary with the right bot_id and a full response
        response = self.client.get(
            self.url, {"bot_id": self.bot.bot_id, "email": self.encrypted_email}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_json = response.json()
        self.assertIsInstance(response_json, dict)
        self.assertEqual(response_json["bot_id"], self.bot.bot_id)
        self.assertEqual(response_json["history"], [])

    def test_fetch_chat_history_with_history_works(self):
        # API should work, return a dictionary with the right bot_id and a full response
        ChatHistory.objects.create(
            user=self.user, bot=self.bot, history=self.valid_history
        )

        response = self.client.get(
            self.url, {"bot_id": self.bot.bot_id, "email": self.encrypted_email}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_json = response.json()
        self.assertIsInstance(response_json, dict)
        self.assertEqual(response_json["bot_id"], self.bot.bot_id)
        self.assertEqual(response_json["history"], self.valid_history)

    def test_fetch_chat_history_with_history_and_lines_works(self):
        ChatHistory.objects.create(
            user=self.user, bot=self.bot, history=self.valid_history
        )

        response = self.client.get(
            self.url,
            {"bot_id": self.bot.bot_id, "lines": 1, "email": self.encrypted_email},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_json = response.json()
        self.assertIsInstance(response_json, dict)
        self.assertEqual(response_json["bot_id"], self.bot.bot_id)
        self.assertListEqual(response_json["history"], self.valid_history[-1:])

    def test_fetch_chat_history_invalid_bot_id(self):
        response = self.client.get(
            self.url, {"bot_id": -1, "email": self.encrypted_email}
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_fetch_chat_history_non_integer_bot_id(self):
        response = self.client.get(
            self.url, {"bot_id": "invalid", "email": self.encrypted_email}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
