import json
from django.forms import model_to_dict
from django.test import TestCase, Client
from django.urls import reverse

from user_profiles.models import User, UserProfile
from user_profiles.utils import encrypt_email


class TestFetchUserInfo(TestCase):
    def setUp(self):
        self.url = reverse("fetch_user_info")
        self.first_name = "John"
        self.last_name = "Doe"
        self.client = Client()
        self.email = "test@example.com"
        self.user = User(
            email=self.email, first_name=self.first_name, last_name=self.last_name
        )
        self.encrypted_email_hex = encrypt_email(self.user.email).hex()

    def test_fetch_user_info_missing_email(self):
        response = self.client.get(self.url, {})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content), {"error": "email parameter missing"}
        )

    def test_fetch_user_info_invalid_email(self):
        response = self.client.get(self.url, {"email": "invalid_hex_string"})
        self.assertEqual(response.status_code, 400)
        self.assertTrue("ValueError" in json.loads(response.content)["error"])

    def test_fetch_user_info_user_not_found(self):
        response = self.client.get(self.url, {"email": self.encrypted_email_hex})
        self.assertEqual(
            json.loads(response.content),
            {"error": f"User with email {self.email} not found"},
        )

    def test_fetch_user_info_success(self):
        self.user.save()
        response = self.client.get(self.url, {"email": self.encrypted_email_hex})
        self.assertEqual(response.status_code, 200)
        expected_profile_data = model_to_dict(UserProfile.objects.get(user=self.user))
        received_profile_data = json.loads(response.content)
        self.assertEqual(expected_profile_data, received_profile_data)

    def test_fetch_user_info_invalid_key(self):
        invalid_key = "6E3272357538782F413F4428472B4B62"
        encrypted_email_hex = encrypt_email(self.email, key=invalid_key).hex()
        response = self.client.get(self.url, {"email": encrypted_email_hex})
        self.assertEqual(response.status_code, 400)
        self.assertTrue("ValueError" in json.loads(response.content)["error"])

    def test_fetch_user_info_create_profile(self):
        self.user.save()
        response = self.client.get(self.url, {"email": self.encrypted_email_hex})
        self.assertEqual(response.status_code, 200)

        profile = UserProfile.objects.get(user=self.user)
        self.assertIsNotNone(profile)

    def test_fetch_user_info_existing_profile(self):
        self.user.save()
        profile = UserProfile.objects.create(user=self.user)
        response = self.client.get(self.url, {"email": self.encrypted_email_hex})
        self.assertEqual(response.status_code, 200)
        expected_profile_data = model_to_dict(profile)
        received_profile_data = json.loads(response.content)
        self.assertEqual(expected_profile_data, received_profile_data)
