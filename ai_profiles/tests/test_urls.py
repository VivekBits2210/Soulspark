# from django.test import SimpleTestCase
#
# class Test
from django.test import TestCase
from django.urls import reverse


class UrlsTestCase(TestCase):
    def test_index_url(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_create_profile_admin_url(self):
        response = self.client.get(reverse('create_profile_admin'))
        self.assertEqual(response.status_code, 405)  # Should return 405 Method Not Allowed
