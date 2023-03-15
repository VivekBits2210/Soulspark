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
        self.bot_profile_fields = [f.name for f in BotProfile._meta.get_fields() if f.concrete]

        image_path = os.path.join('static', 'trial.jpg')
        with open(image_path, 'rb') as f:
            self.image_content = f.read()

        self.first_valid_bot = {
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
        self.bot_profile = BotProfile.objects.create(**self.first_valid_bot)

        self.second_valid_bot = {
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

    def test_create_profile_admin_view(self):
        url = reverse('create_profile_admin')
        self.first_valid_bot["name"] = "Anotherjane"
        copied_data = copy.deepcopy(self.first_valid_bot)
        copied_data['profile_image'] = "trial1.jpg"
        response = self.client.post(url, json.dumps(copied_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BotProfile.objects.count(), 2)
        self.assertTrue(BotProfile.objects.filter(name=self.first_valid_bot["name"]).exists())