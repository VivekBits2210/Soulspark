import base64
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


class ViewsTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass')
        self.client = Client()
        image_path = os.path.join('static', 'trial.jpg')
        with open(image_path, 'rb') as f:
            self.image_content = f.read()

        self.valid_data = {
            'name': 'Jane',
            'gender': 'F',
            'age': 30,
            'bio': 'I am a chatbot too.',
            'profession': 'Engineer',
            'hobbies': {'hobbies': ['reading', 'cricket']},
            'physical_attributes': {"hair": "black"},
            'favorites': {'color': 'blue', 'food': 'pizza'},
            'profile_image': SimpleUploadedFile("test_serializer.jpg", self.image_content, content_type="image/jpeg")
        }
        self.bot_profile = BotProfile.objects.create(**self.valid_data)
        self.bot_profile.save()

    def test_create_profile_view(self):
        bot_id = self.bot_profile.get_id()
        url = reverse('create_profile')
        data = {
            'bot_id': bot_id,
            'name': 'Karen',
            'age': 25,
            'profession': 'Designer',
        }
        self.client.force_login(self.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"message": "BotProfile updated successfully!"})

        new_bot = BotProfile.objects.get(bot_id=bot_id)
        self.assertEqual(new_bot.name, "Karen")
        self.assertEqual(new_bot.age, 25)
        self.assertEqual(new_bot.profession, "Designer")

    def test_create_profile_admin_view(self):
        url = reverse('create_profile_admin')
        copied_data = copy.deepcopy(self.valid_data)
        copied_data['profile_image'] = "trial1.jpg"
        response = self.client.post(url, json.dumps(copied_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BotProfile.objects.count(), 2)

    def test_fetch_profile_view(self):
        url = reverse('fetch_profile')
        response = self.client.get(url, {'bot_id': self.bot_profile.get_id()})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_dict = response.json()
        self.assertEqual(response_dict['bot_id'], self.bot_profile.get_id())

    def test_fetch_profile_image_only_view(self):
        url = reverse('fetch_profile')
        response = self.client.get(url, {'bot_id': self.bot_profile.get_id(), 'image_only': True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('image/jpeg', response['Content-Type'])
