from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ai_profiles.models import BotProfile
from chat_module.models import UserProfile, ChatHistory, DeletedChatHistory


class ChatModuleTests(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        # Create test UserProfile
        self.user_profile = UserProfile.objects.create(
            user=self.user, timezone="America/New_York"
        )

        # Create test bot profile
        self.bot = BotProfile.objects.create(
            name="TestBot",
            gender="M",
            age=25,
            bio="Test bio",
            profession="Developer",
            hobbies='{"hobbies": ["coding", "reading"]}',
            favorites='{"food": "pizza", "color": "blue"}',
            physical_attributes='{"height": "180cm", "weight": "75kg"}',
        )

        # Create test ChatHistory
        self.chat_history = ChatHistory.objects.create(
            user=self.user,
            bot=self.bot,
            history=[
                {"message": "Hi there!", "sender": "user"},
                {"message": "Hello!", "sender": "bot"},
            ],
            input_chars=17,
            level=1.0,
        )

    def test_fetch_chat_history_no_bot_id(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("fetch_chat_history"))
        self.assertEqual(response.status_code, 400)

    def test_fetch_chat_history_non_integer_bot_id(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("fetch_chat_history"), {"bot_id": "testbot"})
        self.assertEqual(response.status_code, 400)

    def test_fetch_chat_history_lines_not_integer(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(
            reverse("fetch_chat_history"),
            {"bot_id": self.bot.bot_id, "lines": "testlines"},
        )
        self.assertEqual(response.status_code, 400)

    def test_fetch_chat_history_lines_less_than_zero(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(
            reverse("fetch_chat_history"), {"bot_id": self.bot.bot_id, "lines": -1}
        )
        self.assertEqual(response.status_code, 400)

    def test_fetch_chat_history_lines_zero(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(
            reverse("fetch_chat_history"), {"bot_id": self.bot.bot_id, "lines": 0}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["history"]), 0)

    def test_fetch_chat_history_return_correct_lines(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(
            reverse("fetch_chat_history"), {"bot_id": self.bot.bot_id, "lines": 1}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["history"]), 1)

    def test_fetch_chat_history_no_history(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(
            reverse("fetch_chat_history"), {"bot_id": self.bot.bot_id + 1, "lines": 5}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["history"]), 0)

    def test_fetch_chat_history_create_chat_history(self):
        self.client.login(username="testuser", password="testpassword")
        bot = BotProfile.objects.create(
            name="TestBot2",
            gender="M",
            age=30,
            bio="Test bio 2",
            profession="Engineer",
            hobbies='{"hobbies": ["gaming", "traveling"]}',
            favorites='{"food": "sushi", "color": "green"}',
            physical_attributes='{"height": "175cm", "weight": "70kg"}',
        )
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(
            reverse("fetch_chat_history"), {"bot_id": bot.bot_id, "lines": 5}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["history"]), 0)
        self.assertTrue(ChatHistory.objects.filter(user=self.user, bot=bot).exists())

    def test_unmatch_no_bot_id(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(reverse("unmatch"))
        self.assertEqual(response.status_code, 400)

    def test_unmatch_non_integer_bot_id(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(reverse("unmatch"), {"bot_id": "testbot"})
        self.assertEqual(response.status_code, 400)

    def test_unmatch_move_chat_history(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(reverse("unmatch"), {"bot_id": self.bot.bot_id})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            DeletedChatHistory.objects.filter(user=self.user, bot=self.bot).exists()
        )
        self.assertFalse(
            ChatHistory.objects.filter(user=self.user, bot=self.bot).exists()
        )

    def test_unmatch_multiple_chat_histories(self):
        # Create additional ChatHistory for testing
        chat_history2 = ChatHistory.objects.create(
            user=self.user,
            bot=self.bot,
            history=[
                {"message": "How are you?", "sender": "user"},
                {"message": "I am good!", "sender": "bot"},
            ],
            input_chars=26,
            level=1.0,
        )

        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(reverse("unmatch"), {"bot_id": self.bot.bot_id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            DeletedChatHistory.objects.filter(user=self.user, bot=self.bot).count(), 2
        )
        self.assertFalse(
            ChatHistory.objects.filter(user=self.user, bot=self.bot).exists()
        )

    def test_unmatch_deleted_history_intact(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(reverse("unmatch"), {"bot_id": self.bot.bot_id})
        self.assertEqual(response.status_code, 200)

        deleted_chat_history = DeletedChatHistory.objects.filter(
            user=self.user, bot=self.bot
        ).first()
        self.assertListEqual(deleted_chat_history.history, self.chat_history.history)

    def test_unmatch_idempotent_operation(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(reverse("unmatch"), {"bot_id": self.bot.bot_id})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            DeletedChatHistory.objects.filter(user=self.user, bot=self.bot).exists()
        )
        self.assertFalse(
            ChatHistory.objects.filter(user=self.user, bot=self.bot).exists()
        )

        # Attempt to unmatch again, it should not raise any errors and should return a 200 status code
        response = self.client.post(reverse("unmatch"), {"bot_id": self.bot.bot_id})
        self.assertEqual(response.status_code, 200)

    def test_unmatch_nonexistent_bot(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(reverse("unmatch"), {"bot_id": 9999})
        self.assertEqual(response.status_code, 400)

    def test_unmatch_no_history(self):
        # Delete the existing chat history
        self.chat_history.delete()

        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(reverse("unmatch"), {"bot_id": self.bot.bot_id})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            ChatHistory.objects.filter(user=self.user, bot=self.bot).exists()
        )
        self.assertFalse(
            DeletedChatHistory.objects.filter(user=self.user, bot=self.bot).exists()
        )

    def test_fetch_chat_history_no_user_authenticated(self):
        response = self.client.get(
            reverse("fetch_chat_history"), {"bot_id": self.bot.bot_id, "lines": 5}
        )
        self.assertEqual(
            response.status_code, 302
        )  # Redirects to the login page as user is not authenticated

    def test_fetch_chat_history_negative_lines(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(
            reverse("fetch_chat_history"), {"bot_id": self.bot.bot_id, "lines": -5}
        )
        self.assertEqual(response.status_code, 400)

    def test_fetch_chat_history_non_integer_lines(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(
            reverse("fetch_chat_history"), {"bot_id": self.bot.bot_id, "lines": "test"}
        )
        self.assertEqual(response.status_code, 400)

    def test_unmatch_no_user_authenticated(self):
        response = self.client.post(reverse("unmatch"), {"bot_id": self.bot.bot_id})
        self.assertEqual(
            response.status_code, 302
        )  # Redirects to the login page as user is not authenticated

    def test_fetch_chat_history_wrong_bot_id_type(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(
            reverse("fetch_chat_history"), {"bot_id": "wrong_type", "lines": 5}
        )
        self.assertEqual(response.status_code, 400)

    def test_fetch_chat_history_empty_history(self):
        # Delete the existing chat history
        self.chat_history.delete()

        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(
            reverse("fetch_chat_history"), {"bot_id": self.bot.bot_id, "lines": 5}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["history"]), 0)

    def test_fetch_chat_history_multiple_histories(self):
        # Create additional ChatHistory for testing
        chat_history2 = ChatHistory.objects.create(
            user=self.user,
            bot=self.bot,
            history=[
                {"message": "How are you?", "sender": "user"},
                {"message": "I am good!", "sender": "bot"},
            ],
            input_chars=26,
            level=1.0,
        )

        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(
            reverse("fetch_chat_history"), {"bot_id": self.bot.bot_id, "lines": 5}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["history"]), 5)
        self.assertTrue(
            ChatHistory.objects.filter(user=self.user, bot=self.bot).exists()
        )

    def test_fetch_chat_history_all_histories(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("fetch_chat_history"), {"lines": 5})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["history"]), 5)
        self.assertTrue(ChatHistory.objects.filter(user=self.user).exists())

    def test_unmatch_wrong_bot_id_type(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(reverse("unmatch"), {"bot_id": "wrong_type"})
        self.assertEqual(response.status_code, 400)

    def test_unmatch_bot_not_in_history(self):
        # Create a new bot that has no associated chat history
        new_bot = BotProfile.objects.create(
            name="NewBot",
            gender="M",
            age=30,
            bio="I am a new bot.",
            profession="Bot Developer",
            hobbies={},
            favorites={},
            physical_attributes={},
            profile_image="images/newbot.jpg",
        )

        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(reverse("unmatch"), {"bot_id": new_bot.bot_id})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            DeletedChatHistory.objects.filter(user=self.user, bot=new_bot).exists()
        )

    def test_fetch_chat_history_multiple_users(self):
        # Create an additional user and chat history
        user2 = User.objects.create_user(username="testuser2", password="testpassword2")
        chat_history2 = ChatHistory.objects.create(
            user=user2,
            bot=self.bot,
            history=[
                {"message": "How are you?", "sender": "user"},
                {"message": "I am good!", "sender": "bot"},
            ],
            input_chars=26,
            level=1.0,
        )

        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(
            reverse("fetch_chat_history"), {"bot_id": self.bot.bot_id, "lines": 5}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["history"]), 5)
        self.assertNotEqual(response.json()["history"], chat_history2.history)

        self.client.logout()
        self.client.login(username="testuser2", password="testpassword2")
        response = self.client.get(
            reverse("fetch_chat_history"), {"bot_id": self.bot.bot_id, "lines": 5}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["history"]), 2)
        self.assertEqual(response.json()["history"], chat_history2.history)

    def test_unmatch_multiple_users(self):
        # Create an additional user and chat history
        user2 = User.objects.create_user(username="testuser2", password="testpassword2")
        chat_history2 = ChatHistory.objects.create(
            user=user2,
            bot=self.bot,
            history=[
                {"message": "How are you?", "sender": "user"},
                {"message": "I am good!", "sender": "bot"},
            ],
            input_chars=26,
            level=1.0,
        )

        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(reverse("unmatch"), {"bot_id": self.bot.bot_id})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            ChatHistory.objects.filter(user=self.user, bot=self.bot).exists()
        )
        self.assertTrue(
            DeletedChatHistory.objects.filter(user=self.user, bot=self.bot).exists()
        )
        self.assertTrue(ChatHistory.objects.filter(user=user2, bot=self.bot).exists())
        self.assertFalse(
            DeletedChatHistory.objects.filter(user=user2, bot=self.bot).exists()
        )

        self.client.logout()
        self.client.login(username="testuser2", password="testpassword2")
        response = self.client.post(reverse("unmatch"), {"bot_id": self.bot.bot_id})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(ChatHistory.objects.filter(user=user2, bot=self.bot).exists())
        self.assertTrue(
            DeletedChatHistory.objects.filter(user=user2, bot=self.bot).exists()
        )

    def test_fetch_chat_history_invalid_lines(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(
            reverse("fetch_chat_history"), {"bot_id": self.bot.bot_id, "lines": -5}
        )
        self.assertEqual(response.status_code, 400)

        response = self.client.get(
            reverse("fetch_chat_history"),
            {"bot_id": self.bot.bot_id, "lines": "invalid"},
        )
        self.assertEqual(response.status_code, 400)

    def test_unmatch_twice(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(reverse("unmatch"), {"bot_id": self.bot.bot_id})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            ChatHistory.objects.filter(user=self.user, bot=self.bot).exists()
        )
        self.assertTrue(
            DeletedChatHistory.objects.filter(user=self.user, bot=self.bot).exists()
        )

        response = self.client.post(reverse("unmatch"), {"bot_id": self.bot.bot_id})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            ChatHistory.objects.filter(user=self.user, bot=self.bot).exists()
        )
        self.assertTrue(
            DeletedChatHistory.objects.filter(user=self.user, bot=self.bot).exists()
        )

    def test_fetch_chat_history_no_bot_specified(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("fetch_chat_history"), {"lines": 5})
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json()["bot_id"])
        self.assertEqual(len(response.json()["history"]), 5)
