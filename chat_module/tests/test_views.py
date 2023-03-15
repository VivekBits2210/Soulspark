from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.test import TestCase, Client
from django.urls import reverse
from chat_module.models import ChatHistory
from chat_module.tests.utils import create_user_and_profile, create_bot


class ViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user, _ = create_user_and_profile()
        self.bot = create_bot()
        self.chat_history = ChatHistory.objects.create(
            user=self.user, bot=self.bot, history=[]
        )

    def test_index_view(self):
        response = self.client.get(reverse("chat_module_index"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fetch_chat_history_view(self):
        url = reverse("fetch_chat_history")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["bot_id"], None)
        self.assertEqual(response.data["history"], [])

        response = self.client.get(f"{url}?lines=0")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["history"], [])

        response = self.client.get(f"{url}?lines=1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["history"], [])

    def test_unmatch_view(self):
        url = reverse("unmatch")
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=self.user)
        response = self.client.post(f"{url}?bot_id=invalid")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Invalid bot_id")

        response = self.client.post(f"{url}?bot_id=1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.data['message'], f"All chat history for bot 1 and user


class UnauthenticatedViewTestCase(TestCase):
    def test_index_view(self):
        response = self.client.get(reverse("chat_module_index"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fetch_chat_history_view(self):
        url = reverse("fetch_chat_history")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_unmatch_view(self):
        url = reverse("unmatch")
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)


class AuthenticatedViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user, _ = create_user_and_profile()
        self.client.login(username=self.user.username, password="testpass")

    def test_index_view(self):
        response = self.client.get(reverse("chat_module_index"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fetch_chat_history_view(self):
        url = reverse("fetch_chat_history")
        self.client.force_login(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unmatch_view(self):
        url = reverse("unmatch")
        self.client.force_login(user=self.user)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(f"{url}?bot_id=invalid")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Invalid bot_id")

        response = self.client.post(f"{url}?bot_id=1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["message"],
            f"All chat history for bot 1 and user {self.user} has been moved to DeletedChatHistory",
        )

    def tearDown(self):
        self.user.delete()
