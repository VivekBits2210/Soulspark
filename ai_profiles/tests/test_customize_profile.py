import json
import os
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from ai_profiles.models import BotProfile


class BotProfileCustomizeProfileTest(APITestCase):
    def setUp(self):
        self.url = reverse('customize_profile')
        self.user = User.objects.create_user(
            username='tester',
            password='password'
        )
        self.client = Client()

        image_path = os.path.join('static', 'trial.jpg')
        with open(image_path, 'rb') as f:
            self.image_content = f.read()

        self.first_valid_bot_info = {
            'name': 'Jane',
            'gender': 'F',
            'age': 30,
            'bio': 'I am a chatbot too.',
            'profession': 'Engineer',
            'hobbies': {'hobbies': ['reading', 'cricket']},
            'physical_attributes': {"hair": "black"},
            'favorites': {'color': 'blue', 'food': 'pizza'},
            'profile_image': SimpleUploadedFile("test_image.jpg", self.image_content, content_type="image/jpeg")
        }
        self.bot_profile = BotProfile.objects.create(**self.first_valid_bot_info)

        self.modified_data = {
            'bot_id': self.bot_profile.bot_id,
            'name': 'UpdatedBot',
            'bio': 'New bio',
            'age': 25,
            'profession': 'Designer',
            'favorites': {'color': 'black'},
        }

    def test_customize_profile_returns_valid_response(self):
        self.client.force_login(user=self.user)
        response = self.client.post(self.url, data=json.dumps(self.modified_data), content_type='application/json')

        # Response should be valid
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Response should be a valid dictionary and contain bot_id
        response_json = response.json()
        self.assertIsInstance(response_json, dict)
        self.assertIn("bot_id", response_json.keys())

    def test_customize_profile_affects_db(self):
        self.client.force_login(user=self.user)
        response = self.client.post(self.url, data=json.dumps(self.modified_data), content_type='application/json')

        # Response should be valid
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Response should be a valid dictionary and contain bot_id
        response_json = response.json()

        # Customized bot should exist
        self.assertTrue(BotProfile.objects.filter(name=self.modified_data['name']).exists())
        customized_bot = BotProfile.objects.get(name=self.modified_data['name'])

        # Returned bot id should be valid
        returned_bot_id = response_json['bot_id']
        self.assertEqual(customized_bot.bot_id, returned_bot_id)

        # Original bot should exist
        self.assertTrue(BotProfile.objects.filter(name=self.bot_profile.name).exists())

        # No other bots should exist
        self.assertEqual(BotProfile.objects.count(), 2)

        # This should be a unique bot, not the same id as before
        self.assertNotEqual(customized_bot.bot_id, self.bot_profile.bot_id)

    def test_customize_profile_has_correct_attributes(self):
        self.client.force_login(user=self.user)
        response = self.client.post(self.url, data=json.dumps(self.modified_data), content_type='application/json')

        # Response should be valid
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        customized_bot = BotProfile.objects.get(name=self.modified_data['name'])

        # Response should be a valid dictionary and contain bot_id
        response_json = response.json()
        # Assert all new attributes are copied over
        self.assertEqual(customized_bot.name, self.modified_data['name'])
        self.assertEqual(customized_bot.age, self.modified_data['age'])
        self.assertEqual(customized_bot.bio, self.modified_data['bio'])
        self.assertEqual(customized_bot.profession, self.modified_data['profession'])
        self.assertDictEqual(customized_bot.favorites, self.modified_data['favorites'])

        # Assert attributes unmentioned are same as before
        self.assertDictEqual(customized_bot.hobbies, self.bot_profile.hobbies)
        self.assertDictEqual(customized_bot.physical_attributes, self.bot_profile.physical_attributes)

    # TODO: Try creating with false info in JSON

    # TODO: Non-int bot id

    # TODO: Missing bot id

    # TODO: Check history being copied over

    # TODO: Tear down, remove all images?
