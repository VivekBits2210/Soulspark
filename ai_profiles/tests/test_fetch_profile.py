import os
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from ai_profiles.models import BotProfile


class BotProfileFetchViewTest(APITestCase):
    def setUp(self):
        self.url = reverse('fetch_profile')

        self.user = User.objects.create_user(
            username='tester',
            password='password'
        )
        self.bot_profile_fields = [f.name for f in BotProfile._meta.get_fields() if f.concrete]
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

        self.second_valid_bot_info = {
            'name': 'Janet',
            'gender': 'F',
            'age': 22,
            'bio': 'I am a chatbot also',
            'profession': 'Engineer',
            'hobbies': {'hobbies': ['reading', 'cricket']},
            'physical_attributes': {"hair": "black"},
            'favorites': {'color': 'blue', 'food': 'pizza'},
            'profile_image': SimpleUploadedFile("test_serializer.jpg", self.image_content, content_type="image/jpeg")
        }

    def test_fetch_profile_view_works(self):
        # API should work, return a dictionary with the right bot_id and a full response
        response = self.client.get(self.url, {'bot_id': self.bot_profile.get_id()})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_json = response.json()
        self.assertIsInstance(response_json, dict)
        self.assertEqual(response_json['bot_id'], self.bot_profile.get_id())
        self.assertListEqual(sorted(self.bot_profile_fields), sorted(response_json.keys()))

    def test_fetch_profile_view_n_equals_one(self):
        # API should work for n=1, return a list of size 1 and a full response
        n = 1
        response = self.client.get(self.url, {'n': n})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_json = response.json()
        self.assertIsInstance(response_json, list)
        self.assertEqual(len(response_json), 1)

        response_keys = response_json[0].keys()
        self.assertListEqual(sorted(self.bot_profile_fields), sorted(response_keys))

    def test_fetch_profile_view_n_equals_teo(self):
        # API should work for n=1, return a list of size 2 and a full response
        n = 2
        BotProfile.objects.create(**self.second_valid_bot_info)
        response = self.client.get(self.url, {'n': n})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_json = response.json()
        self.assertIsInstance(response_json, list)
        self.assertEqual(len(response_json), 2)

        for index in range(n):
            response_keys = response_json[1].keys()
            self.assertListEqual(sorted(self.bot_profile_fields), sorted(response_keys))

    def test_fetch_profile_without_bot_id(self):
        # API should work and return a random bot with a full response
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_json = response.json()
        self.assertIsInstance(response_json, dict)
        self.assertEqual(response_json['name'], self.bot_profile.name)
        self.assertListEqual(sorted(self.bot_profile_fields), sorted(response_json.keys()))

    def test_fetch_profile_with_bit_id_without_image(self):
        # API call should work and return a full response except the image
        response = self.client.get(self.url, {'bot_id': self.bot_profile.bot_id, 'no_image': True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_json = response.json()
        self.assertIsInstance(response_json, dict)
        self.assertNotIn('profile_image', response_json.keys())
        response_json['profile_image'] = "mock"
        self.assertListEqual(sorted(response_json.keys()), sorted(response_json.keys()))

    def test_fetch_profile_image_only_view(self):
        # API response should contain an image
        url = reverse('fetch_profile')
        response = self.client.get(url, {'bot_id': self.bot_profile.get_id(), 'image_only': True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('image/jpeg', response['Content-Type'])

    def test_fetch_profile_invalid_bot_id(self):
        # Invalid bot id fails
        response = self.client.get(self.url, {'bot_id': -1})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # TODO: Test no-integer bot id

    # TODO: Check other failure messages in fetch_profile and trigger them through a test
