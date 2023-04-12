import json
from django.test import TestCase
from django.test import RequestFactory

from user_profiles.models import User
from user_profiles.utils import encrypt_email, decrypt_email, fetch_user_or_error
# from mysecrets import SALT
from dotenv import dotenv_values
SALT = dotenv_values(".env")['SALT']

class UtilsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.email = "test@example.com"
        self.first_name = "John"
        self.last_name = "Doe"
        self.user = User(
            email=self.email, first_name=self.first_name, last_name=self.last_name
        )
        self.key = SALT
        self.encrypted_email_hex = encrypt_email(self.user.email, self.key).hex()

    def test_decrypt_email(self):
        decrypted_email = decrypt_email(self.encrypted_email_hex)
        self.assertEqual(self.email, decrypted_email)

    def test_fetch_user_or_error_missing_email(self):
        request = self.factory.get("/path", data={})

        response = fetch_user_or_error(request)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content), {"error": "email parameter missing"}
        )

    def test_fetch_user_or_error_invalid_email(self):
        request = self.factory.get("/path", data={"email": "invalid_hex_string"})

        response = fetch_user_or_error(request)

        self.assertEqual(response.status_code, 400)
        self.assertTrue("ValueError" in json.loads(response.content)["error"])

    def test_fetch_user_or_error_user_not_found(self):
        request = self.factory.get("/path", data={"email": self.encrypted_email_hex})

        response = fetch_user_or_error(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content),
            {"error": f"User with email {self.email} not found"},
        )

    def test_fetch_user_or_error_success(self):
        self.user.save()
        request = self.factory.get("/path", data={"email": self.encrypted_email_hex})

        fetched_user = fetch_user_or_error(request)

        self.assertEqual(fetched_user, self.user)
