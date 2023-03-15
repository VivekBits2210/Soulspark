import os
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from ai_profiles.models import BotProfile


class BotProfileTestCase(TestCase):

    def setUp(self):
        self.bot_profile = BotProfile.objects.create(
            name='John',
            gender='M',
            age=25,
            bio='I am a chatbot.',
            profession='AI assistant',
            hobbies={"hobbies": ["reading", "music"]},
            favorites={"color": "blue", "food": "pizza"},
            physical_attributes={"hair": "black"},
            profile_image=SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")
        )

    def test_create_bot_profile(self):
        image_path = os.path.join('static', 'trial.jpg')
        with open(image_path, 'rb') as f:
            image_content = f.read()

        valid_data = {
            'name': 'Jane',
            'gender': 'F',
            'age': 30,
            'bio': 'I am a chatbot too.',
            'profession': 'Engineer',
            'hobbies': {'reading': 'novels', 'sport': 'cricket'},
            'physical_attributes': {"hair":"black"},
            'favorites': {'color': 'blue', 'food': 'pizza'},
            'profile_image': SimpleUploadedFile("test_serializer.jpg", image_content, content_type="image/jpeg")
        }
        bot_profile = BotProfile.objects.create(**valid_data)

        self.assertIsNotNone(bot_profile.bot_id)
        self.assertEqual(bot_profile.name, 'Jane')
        self.assertEqual(bot_profile.gender, 'F')
        self.assertEqual(bot_profile.age, 30)
        self.assertEqual(bot_profile.bio, 'I am a chatbot too.')
        self.assertEqual(bot_profile.profession, 'Engineer')
        self.assertEqual(bot_profile.hobbies, {'reading': 'novels', 'sport': 'cricket'})
        self.assertEqual(bot_profile.physical_attributes, {"hair":"black"})
        self.assertEqual(bot_profile.favorites, {'color': 'blue', 'food': 'pizza'})

    def test_primary_key(self):
        with self.assertRaises(ValidationError):
            BotProfile.objects.create(
                bot_id=self.bot_profile.bot_id,
                name='Bot',
                gender='F',
                age=20,
                bio='I am another chatbot.',
                profession='Assistant',
                hobbies={"hobbies": ["traveling"]},
                physical_attributes={"hair": "black"},
                favorites={"color": "red", "food": "sushi"},
                profile_image=SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")
            )

    def test_get_id(self):
        self.assertEqual(self.bot_profile.get_id(), self.bot_profile.bot_id)

    def test_empty_hobbies(self):
        bot_profile = BotProfile.objects.create(
            name='Bot',
            gender='M',
            age=30,
            bio='I am another chatbot.',
            profession='Assistant',
            hobbies={"hobbies": []},
            favorites={"color": "red", "food": "sushi"},
            physical_attributes = {'eye_color': 'blue'},
            profile_image=SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")
        )
        with self.assertRaises(ValidationError):
            bot_profile.hobbies = "invalid value"
            bot_profile.save()

    def test_invalid_gender(self):
        with self.assertRaises(ValidationError):
            bot_profile = BotProfile.objects.create(
                name='Bot',
                gender='G',
                    age=30,
                bio='I am another chatbot.',
                profession='Assistant',
                hobbies={'hobbies': ['traveling']},
                favorites={'color': 'red', 'food': 'sushi'},
                physical_attributes={"hair": "black"},
                profile_image=SimpleUploadedFile("./static/a.jpg", b"file_content", content_type="image/jpeg")
            )

    def test_invalid_name(self):
        with self.assertRaises(ValidationError):
            bot_profile = BotProfile.objects.create(
                name='Bot 2',
                gender='G',
                age=30,
                bio='I am another chatbot.',
                profession='Assistant',
                hobbies={'hobbies': ['traveling']},
                favorites={'color': 'red', 'food': 'sushi'},
                physical_attributes={"hair": "black"},
                profile_image=SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")
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
                physical_attributes={"hair": "black"},
                profile_image=SimpleUploadedFile("a.txt", b"file_content",
                                                 content_type="text/plain").content_type
            )

    def test_save_method_upload_to(self):
        self.assertTrue(os.path.exists(self.bot_profile.profile_image.path))