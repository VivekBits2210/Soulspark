import os
from django.core.exceptions import ValidationError
from django.test import TestCase
from ai_profiles.models import BotProfile


class BotProfileTestCase(TestCase):
    def setUp(self):
        self.bot_profile = BotProfile.objects.create(
            name="John",
            gender="M",
            age=25,
            bio="I am a chatbot.",
            profession="AI assistant",
            interests="reading and music",
            favorites={"color": "blue", "food": "pizza"},
            physical_attributes={"hair": "black"},
        )

    def test_create_bot_profile(self):
        image_path = os.path.join("static", "trial.jpg")
        with open(image_path, "rb") as f:
            image_content = f.read()

        valid_data = {
            "name": "Jane",
            "gender": "F",
            "age": 30,
            "bio": "I am a chatbot too.",
            "profession": "Engineer",
            "interests": "reading and cricket",
            "physical_attributes": {"hair": "black"},
            "favorites": {"color": "blue", "food": "pizza"},
        }
        bot_profile = BotProfile.objects.create(**valid_data)

        self.assertIsNotNone(bot_profile.bot_id)
        self.assertEqual(bot_profile.name, "Jane")
        self.assertEqual(bot_profile.gender, "F")
        self.assertEqual(bot_profile.age, 30)
        self.assertEqual(bot_profile.bio, "I am a chatbot too.")
        self.assertEqual(bot_profile.profession, "Engineer")
        self.assertEqual(bot_profile.interests, "reading and cricket")
        self.assertEqual(bot_profile.physical_attributes, {"hair": "black"})
        self.assertEqual(bot_profile.favorites, {"color": "blue", "food": "pizza"})

    def test_primary_key(self):
        with self.assertRaises(ValidationError):
            BotProfile.objects.create(
                bot_id=self.bot_profile.bot_id,
                name="Bot",
                gender="F",
                age=20,
                bio="I am another chatbot.",
                profession="Assistant",
                interests="travelling",
                physical_attributes={"hair": "black"},
                favorites={"color": "red", "food": "sushi"},
            )

    def test_id(self):
        self.assertEqual(self.bot_profile.bot_id, self.bot_profile.bot_id)

    def test_invalid_gender(self):
        with self.assertRaises(ValidationError):
            bot_profile = BotProfile.objects.create(
                name="Bot",
                gender="G",
                age=30,
                bio="I am another chatbot.",
                profession="Assistant",
                interests="cricket and running",
                favorites={"color": "red", "food": "sushi"},
                physical_attributes={"hair": "black"},
            )

    def test_invalid_name(self):
        with self.assertRaises(ValidationError):
            bot_profile = BotProfile.objects.create(
                name="Bot 2",
                gender="G",
                age=30,
                bio="I am another chatbot.",
                profession="Assistant",
                interests="running",
                favorites={"color": "red", "food": "sushi"},
                physical_attributes={"hair": "black"},
            )
