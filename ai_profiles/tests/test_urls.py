from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class UrlsTestCase(TestCase):
    def test_index_url(self):
        response = self.client.get(reverse('ai_profiles_index'))
        self.assertEqual(response.status_code, 200)

    def test_customize_profile_cannot_be_called_if_not_logged_in(self):
        response = self.client.get(reverse('customize_profile'))
        self.assertEqual(response.status_code, 302)

    def test_customize_profile_cannot_be_get(self):
        user = User.objects.create_user(
            username='tester',
            password='password'
        )
        self.client.force_login(user=user)
        response = self.client.get(reverse('customize_profile'))
        self.assertEqual(response.status_code, 405)

    def test_create_profile_admin_cannot_be_get(self):
        response = self.client.get(reverse('create_profile_admin'))
        self.assertEqual(response.status_code, 405)
