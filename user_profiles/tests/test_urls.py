from django.test import TestCase
from django.urls import reverse


class MainUrlsTestCase(TestCase):
    def test_post_attribute_api_call_cannot_be_get(self):
        response = self.client.get(reverse("post_attribute"))
        self.assertEqual(response.status_code, 405)
