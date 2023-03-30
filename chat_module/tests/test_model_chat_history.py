from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from ai_profiles.models import BotProfile
from chat_module.models import ChatHistory
from user_profiles.models import User


class ChatHistoryTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(email="email@email.com", first_name="Michael", last_name="Jackson")
        self.bot = BotProfile.objects.create(
            name="John",
            gender="M",
            age=25,
            bio="I am a chatbot.",
            profession="AI assistant",
            interests="music and running",
            favorites={"color": "blue", "food": "pizza"},
            physical_attributes={"hair": "black"},
            profile_image=SimpleUploadedFile(
                "test.jpg", b"file_content", content_type="image/jpeg"
            ),
        )

        self.maximal_data = {
            "user": self.user,
            "age": 21,
            "gender": "M",
            "gender_focus": "F",
            "timezone": "Asia/Kolkata",
            "experience": 1,
            "interests": "reading and gaming",
        }

    def test_create_chat_history(self):
        chat_history = ChatHistory(user=self.user, bot=self.bot, history=[], level=1.0)
        chat_history.save()
        self.assertIsNotNone(chat_history.id)

    def test_invalid_level(self):
        with self.assertRaises(ValidationError):
            history = ChatHistory.objects.create(
                user=self.user, bot=self.bot, history=[], level=0
            )

    def test_chat_history_deletion(self):
        chat_history = ChatHistory.objects.create(
            user=self.user, bot=self.bot, history=[{"message": "x"}], level=1.0
        )
        chat_history_id = chat_history.id
        chat_history.delete()

        with self.assertRaises(ChatHistory.DoesNotExist):
            ChatHistory.objects.get(id=chat_history_id)

    def test_unique_user_bot_pair(self):
        history1 = ChatHistory(
            user=self.user,
            bot=self.bot,
            history=[{"key": "value1"}],
        )
        history1.save()

        # Saving a second DeletedChatHistory instance with the same (user, bot) pair should raise an IntegrityError
        with self.assertRaises(ValidationError):
            history2 = ChatHistory(
                user=self.user,
                bot=self.bot,
                history=[{"key": "value2"}],
            )
            history2.save()
