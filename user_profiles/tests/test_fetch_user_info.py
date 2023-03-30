import json
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
from django.forms import model_to_dict
from django.test import TestCase
from rest_framework.test import APIRequestFactory

from user_profiles.models import User, UserProfile
from user_profiles.utils import fetch_user_or_error
from user_profiles.views.fetch_user_info import fetch_user_info
from mysecrets import SALT


class TestFetchUserInfo(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.email = "test@example.com"
        self.first_name = "John"
        self.last_name = "Doe"

    def test_fetch_user_info_missing_email(self):
        request = self.factory.get('/path', data={})

        response = fetch_user_info(request)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), {'error': 'email parameter missing'})

    def test_fetch_user_info_invalid_email(self):
        request = self.factory.get('/path', data={'email': 'invalid_hex_string'})

        response = fetch_user_info(request)

        self.assertEqual(response.status_code, 400)
        self.assertTrue('ValueError' in json.loads(response.content)['error'])

    def test_fetch_user_info_user_not_found(self):
        user = User(email=self.email, first_name=self.first_name, last_name=self.last_name)
        key = SALT.encode('utf-8')
        iv = get_random_bytes(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        padded_email = pad(user.email.encode('utf-8'), AES.block_size)
        ciphertext = cipher.encrypt(padded_email)
        encrypted_email = iv + ciphertext
        encrypted_email_hex = encrypted_email.hex()

        request = self.factory.get('/path', data={'email': encrypted_email_hex})

        response = fetch_user_or_error(request)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), {'error': f'User with email {self.email} not found'})

    def test_fetch_user_info_success(self):
        user = User.objects.create(email=self.email, first_name=self.first_name, last_name=self.last_name)
        key = SALT.encode('utf-8')
        iv = get_random_bytes(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        padded_email = pad(user.email.encode('utf-8'), AES.block_size)
        ciphertext = cipher.encrypt(padded_email)
        encrypted_email = iv + ciphertext
        encrypted_email_hex = encrypted_email.hex()

        request = self.factory.get('/path', data={'email': encrypted_email_hex})

        response = fetch_user_info(request)

        self.assertEqual(response.status_code, 200)

        expected_profile_data = model_to_dict(UserProfile.objects.get(user=user))
        received_profile_data = json.loads(response.content)

        self.assertEqual(expected_profile_data, received_profile_data)

        def test_fetch_user_info_invalid_key(self):
            user = User.objects.create(email=self.email, first_name=self.first_name, last_name=self.last_name)
        key = b'INVALID_KEY'
        iv = get_random_bytes(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        padded_email = pad(user.email.encode('utf-8'), AES.block_size)
        ciphertext = cipher.encrypt(padded_email)
        encrypted_email = iv + ciphertext
        encrypted_email_hex = encrypted_email.hex()

        request = self.factory.get('/path', data={'email': encrypted_email_hex})

        response = fetch_user_info(request)

        self.assertEqual(response.status_code, 400)
        self.assertTrue('ValueError' in json.loads(response.content)['error'])

    def test_fetch_user_info_create_profile(self):
        user = User.objects.create(email=self.email, first_name=self.first_name, last_name=self.last_name)
        key = SALT.encode('utf-8')
        iv = get_random_bytes(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        padded_email = pad(user.email.encode('utf-8'), AES.block_size)
        ciphertext = cipher.encrypt(padded_email)
        encrypted_email = iv + ciphertext
        encrypted_email_hex = encrypted_email.hex()

        request = self.factory.get('/path', data={'email': encrypted_email_hex})

        response = fetch_user_info(request)

        self.assertEqual(response.status_code, 200)

        profile = UserProfile.objects.get(user=user)
        self.assertIsNotNone(profile)

    def test_fetch_user_info_existing_profile(self):
        user = User.objects.create(email=self.email, first_name=self.first_name, last_name=self.last_name)
        profile = UserProfile.objects.create(user=user)
        key = SALT.encode('utf-8')
        iv = get_random_bytes(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        padded_email = pad(user.email.encode('utf-8'), AES.block_size)
        ciphertext = cipher.encrypt(padded_email)
        encrypted_email = iv + ciphertext
        encrypted_email_hex = encrypted_email.hex()

        request = self.factory.get('/path', data={'email': encrypted_email_hex})

        response = fetch_user_info(request)

        self.assertEqual(response.status_code, 200)

        expected_profile_data = model_to_dict(profile)
        received_profile_data = json.loads(response.content)

        self.assertEqual(expected_profile_data, received_profile_data)
