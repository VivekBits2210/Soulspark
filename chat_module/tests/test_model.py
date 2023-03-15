from django.test import TestCase
from chat_module.models import ChatHistory, DeletedChatHistory
from chat_module.tests.utils import create_user, create_bot


class ModelTestCase(TestCase):
    def setUp(self):
        self.user = create_user()
        self.bot = create_bot()
        self.chat_history = ChatHistory.objects.create(
            user=self.user, bot=self.bot, history=[]
        )
        self.deleted_chat_history = DeletedChatHistory.objects.create(
            user=self.user, bot=self.bot, history=[]
        )

    def tearDown(self):
        self.user.delete()
        self.bot.delete()
        self.chat_history.delete()
        self.deleted_chat_history.delete()
