from django.test import TestCase
from django.urls import reverse

from user_profiles.models import User


class UrlsTestCase(TestCase):
    def test_unmatch_api_cannot_be_get(self):
        user = User.objects.create(email="email@email.com", first_name="John", last_name="Galt")
        response = self.client.get(reverse("unmatch"))
        self.assertEqual(response.status_code, 405)
