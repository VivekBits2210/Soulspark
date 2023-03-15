from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount
from chat_module.models import UserProfile
import json


class FetchUserTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="tester", password="password"
        )
        self.email = EmailAddress.objects.create(
            user=self.user, email="testuser@example.com", verified=True, primary=True
        )
        self.social_account = SocialAccount.objects.create(
            provider="facebook", uid="1234", user=self.user
        )
        self.profile = UserProfile.objects.create(user=self.user, age=25, gender="M")

    def test_fetch_user_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("fetch_user_info"))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode("utf-8"))
        self.assertEqual(data["email"], "testuser@example.com")
        self.assertEqual(data["uid"], "1234")
        self.assertEqual(data["age"], 25)
        self.assertEqual(data["gender"], "M")
        self.assertEqual(data["experience"], 0)


class PostAttributeTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser", password="password123"
        )
        self.profile = UserProfile.objects.create(
            user=self.user, age=25, gender="M", experience=100
        )

    def test_post_age_attribute(self):
        self.client.force_login(self.user)
        data = {"age": 30}
        response = self.client.post(
            reverse("post_attribute"),
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.age, 30)

    def test_post_gender_attribute(self):
        self.client.force_login(self.user)
        data = {"gender": "F"}
        response = self.client.post(
            reverse("post_attribute"),
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.gender, "F")

    def test_post_exp_attribute(self):
        self.client.force_login(self.user)
        data = {"experience": 2500}
        response = self.client.post(
            reverse("post_attribute"),
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.experience, 2500)

    def test_post_incorrect_attribute_key(self):
        self.client.force_login(self.user)
        data = {"invalid_key": "value"}
        response = self.client.post(
            reverse("post_attribute"),
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(
            response.json(),
            {
                "error": "Attributes ['invalid_key'] are not valid UserProfile attributes"
            },
        )

    # TODO:Test multiple attribute push, all fine
    def test_post_multiple_valid_attributes(self):
        self.client.force_login(self.user)
        data = {"experience": 2500, "gender": "F"}
        response = self.client.post(
            reverse("post_attribute"),
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.gender, "F")
        self.assertEqual(self.profile.experience, 2500)

    # TODO:Test multiple attributes, some of which are not fine
    def test_post_multiple_attributes_some_invalid(self):
        self.client.force_login(self.user)
        data = {"experience": 2500, "gender": "F", "invalid_key": "invalid_value"}
        response = self.client.post(
            reverse("post_attribute"),
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(
            response.json(),
            {
                "error": "Attributes ['invalid_key'] are not valid UserProfile attributes"
            },
        )
        self.profile.refresh_from_db()

        # None of the updates have happened
        self.assertEqual(self.profile.experience, 100)
        self.assertEqual(self.profile.gender, "M")
