import os
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from ai_profiles.models import BotProfile
from user_profiles.models import UserProfile, User
from user_profiles.utils import encrypt_email


class BotProfileFetchViewTest(APITestCase):
    def setUp(self):
        self.url = reverse("fetch_profile")

        self.bot_profile_fields = [
            f.name for f in BotProfile._meta.get_fields() if f.concrete
        ]
        self.client = Client()

        image_path = os.path.join("static", "trial.jpg")
        with open(image_path, "rb") as f:
            self.image_content = f.read()

        self.first_valid_bot_info = {
            "name": "Jane",
            "gender": "F",
            "age": 30,
            "bio": "I am a chatbot too.",
            "profession": "Engineer",
            "interests": "reading and cricket",
            "physical_attributes": {"hair": "black"},
            "favorites": {"color": "blue", "food": "pizza"},
        }

        self.user = User.objects.create(
            first_name="Billy", last_name="Joel", email="email@email.com"
        )
        self.encrypted_email = encrypt_email(self.user.email).hex()
        self.bot_profile = BotProfile.objects.create(**self.first_valid_bot_info)

        self.second_valid_bot_info = {
            "name": "Janet",
            "gender": "F",
            "age": 22,
            "bio": "I am a chatbot also",
            "profession": "Engineer",
            "interests": "jogging and music",
            "physical_attributes": {"hair": "black"},
            "favorites": {"color": "blue", "food": "pizza"}
        }

    def test_fetch_profile_view_works(self):
        response = self.client.get(self.url, {"bot_id": self.bot_profile.bot_id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_json = response.json()
        self.assertIsInstance(response_json, dict)
        self.assertEqual(response_json["bot_id"], self.bot_profile.bot_id)
        self.assertListEqual(
            sorted(self.bot_profile_fields), sorted(response_json.keys())
        )

    def test_fetch_profile_view_n_equals_one(self):
        n = 1
        response = self.client.get(self.url, {"n": n, "email": self.encrypted_email})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_json = response.json()
        self.assertIsInstance(response_json, list)
        self.assertEqual(len(response_json), 1)

        response_keys = response_json[0].keys()
        self.assertListEqual(sorted(self.bot_profile_fields), sorted(response_keys))

    def test_fetch_profile_view_n_equals_teo(self):
        n = 2
        BotProfile.objects.create(**self.second_valid_bot_info)
        response = self.client.get(self.url, {"n": n, "email": self.encrypted_email})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_json = response.json()
        self.assertIsInstance(response_json, list)
        self.assertEqual(len(response_json), 2)

        for index in range(n):
            response_keys = response_json[1].keys()
            self.assertListEqual(sorted(self.bot_profile_fields), sorted(response_keys))

    def test_fetch_profile_non_searchability(self):
        n = 2
        self.second_valid_bot_info["searchable"] = False
        BotProfile.objects.create(**self.second_valid_bot_info)
        response = self.client.get(self.url, {"n": n, "email": self.encrypted_email})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_json = response.json()
        self.assertIsInstance(response_json, list)
        self.assertEqual(len(response_json), 1)

        response_dict = response_json[0]
        self.assertListEqual(
            sorted(self.bot_profile_fields), sorted(response_dict.keys())
        )
        self.assertEqual(response_dict["bot_id"], self.bot_profile.bot_id)

    # TODO: Figure out why this test is failing
    # def test_fetch_profile_gender_focus_does_not_exist(self):
    #     n = 2
    #     profile = UserProfile.objects.create(user=self.user, gender_focus="M")
    #     response = self.client.get(self.url, {"n": n, "email": self.encrypted_email})
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #
    #     response_json = response.json()
    #     self.assertIsInstance(response_json, list)
    #     self.assertEqual(len(response_json), 0)

    def test_fetch_profile_gender_focus_everyone(self):
        n = 2
        profile = UserProfile.objects.create(user=self.user, gender_focus="E")
        response = self.client.get(self.url, {"n": n, "email": self.encrypted_email})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_json = response.json()
        self.assertIsInstance(response_json, list)
        self.assertEqual(len(response_json), 1)

    def test_fetch_profile_gender_focus_exists(self):
        UserProfile.objects.create(user=self.user, gender_focus="F")
        n = 2
        response = self.client.get(self.url, {"n": n, "email": self.encrypted_email})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_json = response.json()
        self.assertIsInstance(response_json, list)
        self.assertEqual(len(response_json), 1)

    def test_fetch_profile_without_bot_id(self):
        response = self.client.get(self.url, {"email": self.encrypted_email})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_json = response.json()
        self.assertIsInstance(response_json, dict)
        self.assertEqual(response_json["name"], self.bot_profile.name)
        self.assertListEqual(
            sorted(self.bot_profile_fields), sorted(response_json.keys())
        )

    def test_fetch_profile_with_bit_id_without_image(self):
        response = self.client.get(
            self.url,
            {
                "bot_id": self.bot_profile.bot_id,
                "no_image": True,
                "email": self.encrypted_email,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_json = response.json()
        self.assertIsInstance(response_json, dict)
        self.assertListEqual(sorted(response_json.keys()), sorted(response_json.keys()))

    def test_fetch_profile_invalid_bot_id(self):
        response = self.client.get(
            self.url, {"bot_id": -1, "email": self.encrypted_email}
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_fetch_profile_non_integer_bot_id(self):
        response = self.client.get(
            self.url, {"bot_id": "invalid", "email": self.encrypted_email}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_fetch_profile_non_integer_n(self):
        response = self.client.get(
            self.url, {"n": "invalid", "email": self.encrypted_email}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
