from django.test import TestCase
from django.urls import reverse


class UrlsTestCase(TestCase):
    def test_index_url(self):
        response = self.client.get(reverse("ai_profiles_index"))
        self.assertEqual(response.status_code, 200)

    def test_customize_profile_cannot_be_called_if_not_logged_in(self):
        response = self.client.get(reverse("customize_profile"))
        self.assertEqual(response.status_code, 302)

    def test_fetch_profile_cannot_be_called_if_not_logged_in(self):
        response = self.client.get(reverse("fetch_profile"))
        self.assertEqual(response.status_code, 302)

    def test_customize_profile_cannot_be_get(self):
        response = self.client.get(reverse("customize_profile"))
        self.assertEqual(response.status_code, 405)
