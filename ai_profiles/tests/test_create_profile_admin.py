import copy
import json
import os
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from ai_profiles.models import BotProfile


class BotProfileCreateProfileAdminTest(APITestCase):
    def setUp(self):
        self.url = reverse("customize_profile")
        self.user = User.objects.create_user(username="tester", password="password")
        self.client = Client()

        image_path = os.path.join("static", "trial.jpg")
        with open(image_path, "rb") as f:
            self.image_content = f.read()

        self.valid_bot_info = {
            "name": "Jane",
            "gender": "F",
            "age": 30,
            "bio": "I am a chatbot too.",
            "profession": "Engineer",
            "interests": "reading and cricket",
            "physical_attributes": {"hair": "black"},
            "favorites": {"color": "blue", "food": "pizza"},
            "profile_image": "trial.jpg",
        }

    def test_create_profile_admin_view(self):
        url = reverse("create_profile_admin")
        response = self.client.post(
            url, self.valid_bot_info, content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BotProfile.objects.count(), 1)
        self.assertTrue(
            BotProfile.objects.filter(name=self.valid_bot_info["name"]).exists()
        )
        bot = BotProfile.objects.get(name=self.valid_bot_info["name"])
        self.assertEqual(bot.gender, self.valid_bot_info["gender"])
        self.assertEqual(bot.age, self.valid_bot_info["age"])
        self.assertEqual(bot.bio, self.valid_bot_info["bio"])
        self.assertEqual(bot.profession, self.valid_bot_info["profession"])
        self.assertEqual(bot.interests, self.valid_bot_info["interests"])
        self.assertEqual(
            bot.physical_attributes, self.valid_bot_info["physical_attributes"]
        )
        self.assertEqual(bot.favorites, self.valid_bot_info["favorites"])

        # The image is picked up from static folder and then stored, these values will not be equal
        self.assertNotEqual(bot.profile_image, self.valid_bot_info["profile_image"])
