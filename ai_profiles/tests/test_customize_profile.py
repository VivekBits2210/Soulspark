import json
import os
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from ai_profiles.models import BotProfile
from chat_module.models import ChatHistory
from user_profiles.models import User
from user_profiles.utils import encrypt_email


class BotProfileCustomizeProfileTest(APITestCase):
    def setUp(self):
        self.url = reverse("customize_profile")
        self.client = Client()

        image_path = os.path.join("static", "trial.jpg")
        with open(image_path, "rb") as f:
            self.image_content = f.read()

        self.first_valid_bot_info = {
            "name": "Jane",
            "gender": "F",
            "age": 30,
            "bio": "I am a chatbot too.",
            "profession": "Engineer",
            "interests": "reading and cricket",
            "physical_attributes": {"hair": "black"},
            "favorites": {"color": "blue", "food": "pizza"},
            "profile_image": SimpleUploadedFile(
                "test_image.jpg", self.image_content, content_type="image/jpeg"
            ),
        }
        self.bot_profile = BotProfile.objects.create(**self.first_valid_bot_info)
        self.user = User.objects.create(first_name="John", last_name="Doe", email="email@email.com")

        self.modified_data = {
            "bot_id": self.bot_profile.bot_id,
            "name": "UpdatedBot",
            "bio": "New bio",
            "age": 25,
            "profession": "Designer",
            "favorites": {"color": "black"},
            "email": encrypt_email(self.user.email).hex(),
        }

        self.response = self.client.post(
            self.url,
            data=json.dumps(self.modified_data),
            content_type="application/json",
        )

    def test_customize_profile_returns_valid_response(self):
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

        response_json = self.response.json()
        self.assertIsInstance(response_json, dict)
        self.assertIn("bot_id", response_json.keys())

    def test_customize_profile_affects_db(self):
        response_json = self.response.json()

        # Customized bot should exist
        self.assertTrue(
            BotProfile.objects.filter(name=self.modified_data["name"]).exists()
        )
        customized_bot = BotProfile.objects.get(name=self.modified_data["name"])

        # Returned bot id should be valid
        returned_bot_id = response_json["bot_id"]
        self.assertEqual(customized_bot.bot_id, returned_bot_id)

        # Original bot should exist
        self.assertTrue(BotProfile.objects.filter(name=self.bot_profile.name).exists())

        # No other bots should exist
        self.assertEqual(BotProfile.objects.count(), 2)

        # This should be a unique bot, not the same id as before
        self.assertNotEqual(customized_bot.bot_id, self.bot_profile.bot_id)

        # Chat History Object should exist
        history_queryset = ChatHistory.objects.filter(
            user=self.user, bot=customized_bot
        )
        self.assertTrue(history_queryset.exists())

    def test_customize_profile_has_correct_attributes(self):
        customized_bot = BotProfile.objects.get(name=self.modified_data["name"])

        # Assert all new attributes are copied over
        self.assertEqual(customized_bot.name, self.modified_data["name"])
        self.assertEqual(customized_bot.age, self.modified_data["age"])
        self.assertEqual(customized_bot.bio, self.modified_data["bio"])
        self.assertEqual(customized_bot.profession, self.modified_data["profession"])
        self.assertDictEqual(customized_bot.favorites, self.modified_data["favorites"])

        # Assert attributes unmentioned are same as before
        self.assertEqual(customized_bot.interests, self.bot_profile.interests)
        self.assertDictEqual(
            customized_bot.physical_attributes, self.bot_profile.physical_attributes
        )

    def test_history_copied_over(self):
        old_history = {"sample_history_key": "sample_history_value"}
        ChatHistory.objects.create(
            user=self.user, bot=self.bot_profile, history=old_history
        )
        self.response = self.client.post(
            self.url,
            data=json.dumps(self.modified_data),
            content_type="application/json",
        )
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

        response_json = self.response.json()
        self.assertIsInstance(response_json, dict)
        self.assertIn("bot_id", response_json.keys())

        # Customized bot should exist
        returned_id = response_json["bot_id"]
        self.assertTrue(BotProfile.objects.filter(bot_id=returned_id).exists())
        customized_bot = BotProfile.objects.get(bot_id=returned_id)

        # Chat History Object should exist
        history_queryset = ChatHistory.objects.filter(
            user=self.user, bot=customized_bot
        )
        self.assertTrue(history_queryset.exists())
        self.assertEqual(history_queryset.count(), 1)
        self.assertEqual(history_queryset.first().history, old_history)

    def test_missing_bot_id_attribute_invalid(self):
        self.modified_data["incorrect_attribute"] = "incorrect_value"
        self.response = self.client.post(
            self.url,
            data=json.dumps(self.modified_data),
            content_type="application/json",
        )
        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_string_bot_id_cannot_be_non_integer(self):
        self.modified_data["bot_id"] = "invalid"
        self.response = self.client.post(
            self.url,
            data=json.dumps(self.modified_data),
            content_type="application/json",
        )
        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_string_bot_id_cannot_be_missing(self):
        del self.modified_data["bot_id"]
        self.response = self.client.post(
            self.url,
            data=json.dumps(self.modified_data),
            content_type="application/json",
        )
        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)
