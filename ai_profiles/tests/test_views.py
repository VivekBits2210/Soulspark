from django.test import Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from ai_profiles.models import BotProfile


class ViewsTest(APITestCase):
    def setUp(self):
        self.client = Client()
        self.bot_profile = BotProfile.objects.create(
            name="Bot",
            gender="M",
            age=30,
            profession="programmer",
            hobbies={"hobbies":["Reading"]},
            favorites={"food":"pizza"},
            physical_attributes={"hair":"black"}
        )

    def test_create_profile_view(self):
        url = reverse('create_profile')
        data = {
            'bot_id': self.bot_profile.id,
            'name': 'New Bot Name',
            'age': 25,
            'profession': 'Designer',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"message": "BotProfile updated successfully!"})

    def test_create_profile_admin_view(self):
        url = reverse('create_profile_admin')
        data = {
            'name': 'Bot 2',
            'gender': 'F',
            'age': 35,
            'profession': 'Teacher',
            'hobbies': {'hobbies':['Swimming']},
            'favorites': 'Ice cream',
            'physical_attributes': {"hair":"black"},
            'bio': "Test bio"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BotProfile.objects.count(), 2)

    def test_fetch_profile_view(self):
        url = reverse('fetch_profile')
        response = self.client.get(url, {'bot_id': self.bot_profile.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['bot_id'], self.bot_profile.id)

    def test_fetch_profile_image_only_view(self):
        url = reverse('fetch_profile')
        response = self.client.get(url, {'bot_id': self.bot_profile.id, 'image_only': True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('image/jpeg', response['Content-Type'])
