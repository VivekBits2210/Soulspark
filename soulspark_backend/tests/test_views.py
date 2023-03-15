from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount
from chat_module.models import UserProfile
import json


class FetchUserTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser", password="password123"
        )
        self.email = EmailAddress.objects.create(
            user=self.user, email="testuser@example.com", verified=True, primary=True
        )
        self.social_account = SocialAccount.objects.create(
            provider="facebook", uid="1234", user=self.user
        )
        self.profile = UserProfile.objects.create(
            user=self.user, age=25, gender="M", level="Beginner"
        )

    def test_fetch_user_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("fetch-user-info"))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode("utf-8"))
        self.assertEqual(data["username"], "testuser")
        self.assertEqual(data["email"], "testuser@example.com")
        self.assertEqual(data["uid"], "1234")
        self.assertEqual(data["age"], 25)
        self.assertEqual(data["gender"], "M")
        self.assertEqual(data["level"], "Beginner")

    def test_fetch_user_unauthenticated(self):
        response = self.client.get(reverse("fetch-user-info"))
        self.assertRedirects(response, "/accounts/login/?next=/fetch-user-info/")


class PostAttributeTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser", password="password123"
        )
        self.profile = UserProfile.objects.create(
            user=self.user, age=25, gender="M", level="Beginner"
        )

    def test_post_age_attribute(self):
        self.client.force_login(self.user)
        data = {"key": "age", "value": 30}
        response = self.client.post(
            reverse("post-attribute"), json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.age, 30)

    def test_post_gender_attribute(self):
        self.client.force_login(self.user)
        data = {"key": "gender", "value": "F"}
        response = self.client.post(
            reverse("post-attribute"), json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.gender, "F")

    def test_post_level_attribute(self):
        self.client.force_login(self.user)
        data = {"key": "level", "value": "Intermediate"}
        response = self.client.post(
            reverse("post-attribute"), json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.level, "Intermediate")

    def test_post_incorrect_attribute_key(self):
        self.client.force_login(self.user)
        data = {"key": "invalid_key", "value": "value"}
        response = self.client.post(
            reverse("post-attribute"), json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"error": "Invalid attribute key"})
