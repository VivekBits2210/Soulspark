import os
import io
from unittest import skip

from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase
from ai_profiles.serializers import BotProfileSerializer


class BotProfileSerializerTestCase(APITestCase):
    def setUp(self):
        image_path = os.path.join("static", "trial.jpg")
        with open(image_path, "rb") as f:
            image_content = f.read()

        self.valid_data = {
            "name": "Bot",
            "gender": "M",
            "age": 30,
            "bio": "I am Bot1",
            "profession": "Engineer",
            "interests": "chess and cricket",
            "physical_attributes": {"hair": "black"},
            "favorites": {"color": "blue", "food": "pizza"},
        }

    def test_create_valid_bot_profile(self):
        serializer = BotProfileSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        profile = serializer.save()
        self.assertIsNotNone(profile.bot_id)
        self.assertEqual(profile.name, self.valid_data["name"])
        self.assertEqual(profile.gender, self.valid_data["gender"])
        self.assertEqual(profile.age, self.valid_data["age"])
        self.assertEqual(profile.bio, self.valid_data["bio"])
        self.assertEqual(profile.profession, self.valid_data["profession"])
        self.assertEqual(profile.interests, self.valid_data["interests"])
        self.assertEqual(profile.favorites, self.valid_data["favorites"])

    def test_missing_required_fields(self):
        invalid_data = {
            "name": "Bot1",
            "gender": "M",
            "age": 30,
        }
        serializer = BotProfileSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            set(serializer.errors.keys()),
            {
                "name",
                "bio",
                "profession",
                "profile_image",
            },
        )
