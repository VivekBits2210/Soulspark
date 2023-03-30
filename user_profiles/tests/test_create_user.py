from django.test import TestCase, Client
from django.urls import reverse
import json

from user_profiles.utils import encrypt_email
from user_profiles.models import User


class TestCreateUser(TestCase):
    def setUp(self):
        self.url = reverse("create_user")
        self.email = 'test@example.com'
        self.first_name = 'John'
        self.last_name = 'Doe'
        self.client = Client()
        self.email = "email@email.com"
        self.user = User(
            email=self.email, first_name="Joe", last_name="Mama"
        )
        self.encrypted_email_hex = encrypt_email(self.user.email).hex()

    def test_create_user_success(self):
        data = {
            'email': self.encrypted_email_hex,
            'first_name': self.first_name,
            'last_name': self.last_name,
        }
        response = self.client.post(
            self.url,
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)

        user = User.objects.get(email=self.email)
        self.assertIsNotNone(user)
        self.assertEqual(user, self.user)

    def test_create_user_missing_email(self):
        data = {
            'first_name': self.first_name,
            'last_name': self.last_name,
        }
        response = self.client.post(
            self.url,
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertTrue('email' in json.loads(response.content)['error'])

    def test_create_user_invalid_email(self):
        encrypted_email_hex = 'INVALID_EMAIL_HEX'

        data = {
            'email': encrypted_email_hex,
            'first_name': self.first_name,
            'last_name': self.last_name,
        }
        response = self.client.post(
            self.url,
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertTrue('ValueError' in json.loads(response.content)['error'])

    def test_create_user_existing_email(self):
        data = {
            'email': self.encrypted_email_hex,
            'first_name': self.first_name,
            'last_name': self.last_name,
        }

        response = self.client.post(
            self.url,
            data=json.dumps(data),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)

    def test_create_user_missing_first_name(self):
        data = {
            'email': self.encrypted_email_hex,
            'last_name': self.last_name,
        }

        response = self.client.post(
            self.url,
            data=json.dumps(data),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)

    def test_create_user_missing_last_name(self):
        data = {
            'email': self.encrypted_email_hex,
            'first_name': self.first_name,
        }

        response = self.client.post(
            self.url,
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())
        self.assertIn('ValidationError', response.json()['error'])

    def test_create_user_duplicate_entry(self):
        data = {
            'email': self.encrypted_email_hex,
            'first_name': self.first_name,
            'last_name': self.last_name,
        }
        response = self.client.post(
            self.url,
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)

        response2 = self.client.post(
            self.url,
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response2.status_code, 400)
        self.assertIn('email', response2.json())

    def test_create_user_with_invalid_email(self):
        invalid_email = "invalid_email@"
        invalid_encrypted_email = encrypt_email(invalid_email).hex()

        data = {
            'email': invalid_encrypted_email,
            'first_name': self.first_name,
            'last_name': self.last_name,
        }
        response = self.client.post(
            self.url,
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('email', response.json())

    def test_create_user_with_missing_email(self):
        data = {
            'first_name': self.first_name,
            'last_name': self.last_name,
        }
        response = self.client.post(
            self.url,
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())


    def test_create_user_duplicate_entry(self):
        data = {
            'email': self.encrypted_email_hex,
            'first_name': self.first_name,
            'last_name': self.last_name,
        }
        response = self.client.post(
            self.url,
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)

        response2 = self.client.post(
            self.url,
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response2.status_code, 400)
        self.assertIn('email', response2.json())

    def test_create_user_with_invalid_email(self):
        data = {
            'email': "email@",
            'first_name': self.first_name,
            'last_name': self.last_name,
        }
        response = self.client.post(
            self.url,
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())
        self.assertIn('ValueError', response.json()['error'])

    def test_create_user_with_missing_email(self):
        data = {
            'first_name': self.first_name,
            'last_name': self.last_name,
        }

        response = self.client.post(
            self.url,
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())
        self.assertIn('email parameter missing', response.json()['error'])

    def test_create_user_with_invalid_encrypted_email(self):
        invalid_encrypted_email = "invalid_eCLSncrypted_email"

        data = {
            'email': invalid_encrypted_email,
            'first_name': self.first_name,
            'last_name': self.last_name,
        }

        response = self.client.post(
            self.url,
            data=json.dumps(data),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())
        self.assertIn('ValueError', response.json()['error'])

    def test_create_user_with_empty_first_name_and_last_name(self):
        data = {
            'email': self.encrypted_email_hex,
            'first_name': '',
            'last_name': '',
        }
        response = self.client.post(
            self.url,
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('first_name', response.json())
        self.assertIn('last_name', response.json())

    def test_create_user_with_extra_fields(self):
        data = {
            'email': self.encrypted_email_hex,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'extra_field': 'extra_value',
        }

        response = self.client.post(
            self.url,
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)

        user = User.objects.get(email=self.email)
        self.assertIsNotNone(user)
        self.assertEqual(user.first_name, self.first_name)
        self.assertEqual(user.last_name, self.last_name)
