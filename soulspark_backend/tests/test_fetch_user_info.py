from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount
from chat_module.models import UserProfile
import json


class FetchUserInfoTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="tester", password="password"
        )
        self.email = EmailAddress.objects.create(
            user=self.user, email="testuser@example.com", verified=True, primary=True
        )
        self.social_account = SocialAccount.objects.create(
            provider="facebook", uid="1234", user=self.user
        )
        self.profile = UserProfile.objects.create(user=self.user, age=25, gender="M")

    def test_fetch_user_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("fetch_user_info"))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode("utf-8"))
        self.assertEqual(data["email"], "testuser@example.com")
        self.assertEqual(data["uid"], "1234")
        self.assertEqual(data["age"], 25)
        self.assertEqual(data["gender"], "M")
        self.assertEqual(data["experience"], 1)
