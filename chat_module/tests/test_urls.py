from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class UrlsTestCase(TestCase):
    def test_index_url(self):
        response = self.client.get(reverse("chat_module_index"))
        self.assertEqual(response.status_code, 200)

    def test_fetch_chat_history_cannot_be_called_if_not_logged_in(self):
        response = self.client.get(reverse("fetch_chat_history"))
        self.assertEqual(response.status_code, 302)

    def test_unmatch_cannot_be_called_if_not_logged_in(self):
        response = self.client.post(reverse("unmatch"))
        self.assertEqual(response.status_code, 302)

    def test_unmatch_api_cannot_be_get(self):
        user = User.objects.create_user(username="tester", password="password")
        self.client.force_login(user=user)
        response = self.client.get(reverse("unmatch"))
        self.assertEqual(response.status_code, 405)
