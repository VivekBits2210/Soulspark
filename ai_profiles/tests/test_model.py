from unittest import skip
import os
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from ai_profiles.models import BotProfile


class BotProfileTestCase(TestCase):

    def setUp(self):
        self.bot_profile = BotProfile.objects.create(
            name='John Doe',
            gender='M',
            age=25,
            bio='I am a chatbot.',
            profession='AI assistant',
            hobbies={"hobbies": ["reading", "music"]},
            favorites={"color": "blue", "food": "pizza"},
            profile_image=SimpleUploadedFile("./static/trial.jpg", b"file_content", content_type="image/jpeg")
        )

    def test_create_bot_profile(self):
        bot_profile = BotProfile.objects.create(
            name='Jane Doe',
            gender='F',
            age=30,
            bio='I am a chatbot too.',
            profession='Virtual assistant',
            hobbies={"hobbies": ["sports", "movies"]},
            favorites={"color": "green", "food": "pasta"},
            profile_image=SimpleUploadedFile("./static/trial.jpg", b"file_content", content_type="image/jpeg")
        )

        self.assertIsNotNone(bot_profile.bot_id)
        self.assertEqual(bot_profile.name, 'Jane Doe')
        self.assertEqual(bot_profile.gender, 'F')
        self.assertEqual(bot_profile.age, 30)
        self.assertEqual(bot_profile.bio, 'I am a chatbot too.')
        self.assertEqual(bot_profile.profession, 'Virtual assistant')
        self.assertEqual(bot_profile.hobbies, {"hobbies": ["sports", "movies"]})
        self.assertEqual(bot_profile.favorites, {'color': 'green', 'food': 'pasta'})

    def test_primary_key(self):
        with self.assertRaises(ValidationError):
            BotProfile.objects.create(
                bot_id=self.bot_profile.bot_id,
                name='Bot 2',
                gender='F',
                age=20,
                bio='I am another chatbot.',
                profession='Assistant',
                hobbies={"hobbies": ["traveling"]},
                favorites={"color": "red", "food": "sushi"},
                profile_image=SimpleUploadedFile("./static/trial.jpg", b"file_content", content_type="image/jpeg")
            )

    def test_get_id(self):
        self.assertEqual(self.bot_profile.get_id(), self.bot_profile.bot_id)

    def test_empty_hobbies(self):
        bot_profile = BotProfile.objects.create(
            name='Bot 2',
            gender='M',
            age=30,
            bio='I am another chatbot.',
            profession='Assistant',
            hobbies={"hobbies": [""]},
            favorites={"color": "red", "food": "sushi"},
            profile_image=SimpleUploadedFile("./static/trial.jpg", b"file_content", content_type="image/jpeg")
        )
        with self.assertRaises(ValidationError):
            bot_profile.hobbies = "invalid value"
            bot_profile.save()

    def test_invalid_gender(self):
        with self.assertRaises(ValidationError):
            bot_profile = BotProfile.objects.create(
                name='Bot 2',
                gender='G',
                age=30,
                bio='I am another chatbot.',
                profession='Assistant',
                hobbies={'hobbies': ['traveling']},
                favorites={'color': 'red', 'food': 'sushi'},
                profile_image=SimpleUploadedFile("./static/a.jpg", b"file_content", content_type="image/jpeg")
            )

    def test_invalid_image(self):
        with self.assertRaises(ValidationError):
            bot_profile = BotProfile.objects.create(
                name='Bot 2',
                gender='M',
                age=30,
                bio='I am another chatbot.',
                profession='Assistant',
                hobbies={'hobbies': ['traveling']},
                favorites={'color': 'red', 'food': 'sushi'},
                profile_image=SimpleUploadedFile("./static/a.txt", b"file_content", content_type="text/plain")
            )

    def test_save_method_upload_to(self):
        self.assertTrue(os.path.exists(self.bot_profile.profile_image.path))

    def tearDown(self):
        # remove all text files and files starting with 'trial' under the 'images' folder
        folder_path = os.path.join('images')
        for filename in os.listdir(folder_path):
            if filename.endswith('.txt') or filename.startswith('trial'):
                file_path = os.path.join(folder_path, filename)
                os.remove(file_path)

        super().tearDown()
