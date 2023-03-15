from django.test import TestCase
from django.contrib.auth import get_user_model
from chat_module.models import UserProfile


class UserProfileTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="password123"
        )

    def test_user_profile_creation(self):
        profile = UserProfile.objects.create(user=self.user)
        self.assertEqual(profile.user, self.user)
        self.assertIsNone(profile.age)
        self.assertIsNone(profile.gender)
        self.assertIsNone(profile.gender_focus)
        self.assertEqual(profile.level, "1")
        self.assertIsNone(profile.interests)
        self.assertTrue(profile.is_active)
        self.assertFalse(profile.is_staff)
