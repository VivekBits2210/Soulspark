from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from chat_module.models import UserProfile


class UserProfileTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="password")

        self.maximal_data = {
            "user": self.user,
            "age": 21,
            "gender": "M",
            "gender_focus": "F",
            "timezone": "Asia/Kolkata",
            "experience": 1,
            "interests": "reading,gaming",
        }

    def test_user_profile_creation_minimal(self):
        profile = UserProfile.objects.create(user=self.user)
        self.assertEqual(profile.user, self.user)
        self.assertIsNone(profile.age)
        self.assertIsNone(profile.gender)
        self.assertEqual(profile.gender_focus, "E")
        self.assertEqual(profile.experience, 1)
        self.assertEqual(profile.interests, "")
        self.assertTrue(profile.is_active)
        self.assertFalse(profile.is_staff)

    def test_user_profile_creation_minimal_with_gender_focus(self):
        profile = UserProfile.objects.create(user=self.user, gender_focus="M")
        self.assertEqual(profile.user, self.user)
        self.assertIsNone(profile.age)
        self.assertIsNone(profile.gender)
        self.assertEqual(profile.gender_focus, "M")
        self.assertEqual(profile.experience, 1)
        self.assertEqual(profile.interests, "")
        self.assertTrue(profile.is_active)
        self.assertFalse(profile.is_staff)

    def test_user_profile_creation_maximal(self):
        profile = UserProfile.objects.create(**self.maximal_data)
        self.assertEqual(profile.user, self.maximal_data["user"])
        self.assertEqual(profile.age, self.maximal_data["age"])
        self.assertEqual(profile.gender, self.maximal_data["gender"])
        self.assertEqual(profile.gender_focus, self.maximal_data["gender_focus"])
        self.assertEqual(profile.experience, self.maximal_data["experience"])
        self.assertEqual(profile.interests, self.maximal_data["interests"])
        self.assertTrue(profile.is_active)
        self.assertFalse(profile.is_staff)

    def test_user_profile_primary_key(self):
        with self.assertRaises(ValidationError):
            UserProfile.objects.create(**self.maximal_data)
            UserProfile.objects.create(user=self.user)

    def test_invalid_gender(self):
        with self.assertRaises(ValidationError):
            UserProfile.objects.create(user=self.user, gender="X")

    def test_invalid_age(self):
        with self.assertRaises(ValidationError):
            UserProfile.objects.create(user=self.user, gender="X", age=12)

    def test_invalid_gender_focus(self):
        with self.assertRaises(ValidationError):
            UserProfile.objects.create(
                user=self.user, gender="M", age=18, gender_focus="X"
            )

    def test_invalid_experience(self):
        with self.assertRaises(ValidationError):
            UserProfile.objects.create(
                user=self.user, gender="M", age=18, gender_focus="F", experience=-1
            )

    def test_invalid_timezone(self):
        with self.assertRaises(ValidationError):
            UserProfile.objects.create(
                user=self.user,
                gender="M",
                age=18,
                gender_focus="F",
                experience=1,
                interests="cooking,cleaning",
                timezone="invalid",
            )
