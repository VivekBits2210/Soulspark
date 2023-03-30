from django.core.exceptions import ValidationError
from django.test import TestCase
from chat_module.models import DeletedChatHistory
from chat_module.tests.utils import create_bot
from user_profiles.models import User


class ChatHistoryTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            email="email@email.com", first_name="Elon", last_name="Musk"
        )
        self.bot = create_bot()
        self.maximal_data = {
            "user": self.user,
            "age": 21,
            "gender": "M",
            "gender_focus": "F  ",
            "timezone": "Asia/Kolkata",
            "experience": 1,
            "interests": "reading and gaming",
        }

    def test_create_chat_history(self):
        chat_history = DeletedChatHistory.objects.create(
            user=self.user, bot=self.bot, history=[], level=1.0
        )
        chat_history.save()
        self.assertIsNotNone(chat_history.id)

    def test_invalid_level(self):
        with self.assertRaises(ValidationError):
            history = DeletedChatHistory.objects.create(
                user=self.user, bot=self.bot, history=[{"key": "value"}], level=0
            )

    def test_chat_history_deletion(self):
        chat_history = DeletedChatHistory.objects.create(
            user=self.user, bot=self.bot, history={"messages": []}, level=1.0
        )

        chat_history_id = chat_history.id
        chat_history.delete()

        with self.assertRaises(DeletedChatHistory.DoesNotExist):
            DeletedChatHistory.objects.get(id=chat_history_id)
