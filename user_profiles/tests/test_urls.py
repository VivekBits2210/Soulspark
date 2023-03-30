
from django.test import TestCase
from django.urls import reverse
from user_profiles.models import User


class MainUrlsTestCase(TestCase):
    def test_post_attribute_cannot_be_called_if_not_logged_in(self):
        response = self.client.get(reverse("post_attribute"))
        self.assertEqual(response.status_code, 302)

    def test_fetch_user_info_cannot_be_called_if_not_logged_in(self):
        response = self.client.post(reverse("fetch_user_info"))
        self.assertEqual(response.status_code, 302)

    def test_post_attribute_api_call_cannot_be_get(self):
        user = User.objects.create(email="email@email.com", first_name="Ezio", last_name="Auditore")
        response = self.client.get(reverse("post_attribute"))
        self.assertEqual(response.status_code, 405)
