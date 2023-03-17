from django.test import Client
from django.urls import reverse
from rest_framework.test import APITestCase

from chat_module.models import ChatHistory, DeletedChatHistory
from chat_module.tests.utils import create_user_and_profile, create_bot


class UnmatchTestCase(APITestCase):
    def setUp(self):
        self.url = reverse("unmatch")
        self.bot = create_bot()
        self.user, self.user_profile = create_user_and_profile()

        self.client = Client()
        self.client.force_login(user=self.user)

        self.valid_history = [
            {"message": "hi", "from": "user"},
            {"message": "hey, how can I help", "from": "bot"},
        ]

    def test_unmatch_works_without_history(self):
        response = self.client.post(self.url, data={"bot_id": self.bot.bot_id})
        self.assertEqual(response.status_code, 200)

        query_set = ChatHistory.objects.filter(user=self.user, bot=self.bot)
        self.assertFalse(query_set.exists())

    def test_unmatch_works_with_history(self):
        ChatHistory.objects.create(
            user=self.user, bot=self.bot, history=self.valid_history
        )
        response = self.client.post(self.url, data={"bot_id": self.bot.bot_id})
        self.assertEqual(response.status_code, 200)

        deleted_query_set = DeletedChatHistory.objects.filter(
            user=self.user, bot=self.bot
        )
        self.assertTrue(deleted_query_set.exists())
        self.assertEqual(deleted_query_set.count(), 1)

        deleted_history = deleted_query_set.first()
        self.assertEqual(deleted_history.history, self.valid_history)

        query_set = ChatHistory.objects.filter(user=self.user, bot=self.bot)
        self.assertFalse(query_set.exists())

    def test_unmatch_twice(self):
        ChatHistory.objects.create(
            user=self.user, bot=self.bot, history=self.valid_history
        )
        response = self.client.post(self.url, data={"bot_id": self.bot.bot_id})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            ChatHistory.objects.filter(user=self.user, bot=self.bot).exists()
        )
        self.assertTrue(
            DeletedChatHistory.objects.filter(user=self.user, bot=self.bot).exists()
        )

        ChatHistory.objects.create(
            user=self.user, bot=self.bot, history=self.valid_history
        )
        response = self.client.post(self.url, data={"bot_id": self.bot.bot_id})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            ChatHistory.objects.filter(user=self.user, bot=self.bot).exists()
        )
        self.assertTrue(
            DeletedChatHistory.objects.filter(user=self.user, bot=self.bot).exists()
        )

    def test_unmatch_no_bot_id(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 400)

    def test_unmatch_non_integer_bot_id(self):
        response = self.client.post(self.url, data={"bot_id": "testbot"})
        self.assertEqual(response.status_code, 400)

    def test_unmatch_non_existent_bot_id(self):
        response = self.client.post(self.url, data={"bot_id": 999})
        self.assertEqual(response.status_code, 404)
