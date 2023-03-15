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


from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from ai_profiles.models import BotProfile


class UserProfileTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

    def test_create_user_profile(self):
        profile = UserProfile(
            user=self.user,
            age=25,
            gender="M",
            gender_focus="F",
            timezone="America/New_York",
            interests="music,travel",
        )
        profile.save()
        self.assertIsNotNone(profile.id)

    def test_invalid_timezone(self):
        with self.assertRaises(ValidationError):
            timezone_validation("Invalid/TimeZone")

    def test_invalid_gender(self):
        with self.assertRaises(ValidationError):
            gender_validation("X")

    def test_invalid_interests(self):
        with self.assertRaises(ValidationError):
            interests_validation(",music,travel")

    def test_invalid_age(self):
        with self.assertRaises(ValidationError):
            age_validation(12)

    def test_update_user_profile(self):
        profile = UserProfile(
            user=self.user,
            age=25,
            gender="M",
            gender_focus="F",
            timezone="America/New_York",
            interests="music,travel",
        )
        profile.save()

        profile.age = 30
        profile.gender = "F"
        profile.gender_focus = "M"
        profile.timezone = "Europe/London"
        profile.interests = "sports,reading"
        profile.save()

        updated_profile = UserProfile.objects.get(id=profile.id)
        self.assertEqual(updated_profile.age, 30)
        self.assertEqual(updated_profile.gender, "F")
        self.assertEqual(updated_profile.gender_focus, "M")
        self.assertEqual(updated_profile.timezone, "Europe/London")
        self.assertEqual(updated_profile.interests, "sports,reading")

    def test_user_profile_deletion(self):
        profile = UserProfile(
            user=self.user,
            age=25,
            gender="M",
            gender_focus="F",
            timezone="America/New_York",
            interests="music,travel",
        )
        profile.save()

        profile_id = profile.id
        profile.delete()

        with self.assertRaises(UserProfile.DoesNotExist):
            UserProfile.objects.get(id=profile_id)


class ChatHistoryTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.bot = BotProfile.objects.create(
            name="TestBot",
            gender="M",
            age=25,
            bio="This is a test bot.",
            profession="Test Profession",
            hobbies={"travel": "Traveling the world"},
            favorites={"food": "Pizza"},
            physical_attributes={"height": "180cm"},
            profile_image="images/testbot.jpg",
        )

    def test_create_chat_history(self):
        chat_history = ChatHistory(
            user=self.user, bot=self.bot, history={"messages": []}, level=1.0
        )
        chat_history.save()
        self.assertIsNotNone(chat_history.id)

    def test_invalid_level(self):
        with self.assertRaises(ValidationError):
            level_validation(0.5)

        def test_chat_history_update(self):
            chat_history = ChatHistory(
                user=self.user, bot=self.bot, history={"messages": []}, level=1.0
            )

        chat_history.save()

        chat_history.history = {"messages": [{"user": "Hello"}]}
        chat_history.input_chars = 5
        chat_history.level = 1.5
        chat_history.save()

        updated_chat_history = ChatHistory.objects.get(id=chat_history.id)
        self.assertEqual(
            updated_chat_history.history, {"messages": [{"user": "Hello"}]}
        )
        self.assertEqual(updated_chat_history.input_chars, 5)
        self.assertEqual(updated_chat_history.level, 1.5)

    def test_chat_history_deletion(self):
        chat_history = ChatHistory(
            user=self.user, bot=self.bot, history={"messages": []}, level=1.0
        )
        chat_history.save()

        chat_history_id = chat_history.id
        chat_history.delete()

        with self.assertRaises(ChatHistory.DoesNotExist):
            ChatHistory.objects.get(id=chat_history_id)


class DeletedChatHistoryTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.bot = BotProfile.objects.create(
            name="TestBot",
            gender="M",
            age=25,
            bio="This is a test bot.",
            profession="Test Profession",
            hobbies={"travel": "Traveling the world"},
            favorites={"food": "Pizza"},
            physical_attributes={"height": "180cm"},
            profile_image="images/testbot.jpg",
        )

    def test_create_deleted_chat_history(self):
        deleted_chat_history = DeletedChatHistory(
            user=self.user, bot=self.bot, history={"messages": []}
        )
        deleted_chat_history.save()
        self.assertIsNotNone(deleted_chat_history.id)

        def test_deleted_chat_history_update(self):
            deleted_chat_history = DeletedChatHistory(
                user=self.user, bot=self.bot, history={"messages": []}
            )

        deleted_chat_history.save()

        deleted_chat_history.history = {"messages": [{"user": "Goodbye"}]}
        deleted_chat_history.input_chars = 7
        deleted_chat_history.save()

        updated_deleted_chat_history = DeletedChatHistory.objects.get(
            id=deleted_chat_history.id
        )
        self.assertEqual(
            updated_deleted_chat_history.history, {"messages": [{"user": "Goodbye"}]}
        )
        self.assertEqual(updated_deleted_chat_history.input_chars, 7)

    def test_deleted_chat_history_deletion(self):
        deleted_chat_history = DeletedChatHistory(
            user=self.user, bot=self.bot, history={"messages": []}
        )
        deleted_chat_history.save()

        deleted_chat_history_id = deleted_chat_history.id
        deleted_chat_history.delete()

        with self.assertRaises(DeletedChatHistory.DoesNotExist):
            DeletedChatHistory.objects.get(id=deleted_chat_history_id)


class DeletedChatHistoryModelTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.bot = BotProfile.objects.create(
            name="John",
            gender="M",
            age=30,
            bio="I am a chatbot",
            profession="Chatbot",
            hobbies={"Reading": 8, "Dancing": 7},
            favorites={"Food": "Pizza", "Movie": "The Godfather"},
            physical_attributes={"Height": "5'11\"", "Weight": "150 lbs"},
            profile_image="images/john.png",
        )

    def test_deletedchathistory_creation(self):
        deleted_chat_history = DeletedChatHistory.objects.create(
            user=self.user,
            bot=self.bot,
            history=[{"message": "Hi there!", "timestamp": timezone.now()}],
            input_chars=10,
            level=Decimal("1.0"),
        )
        self.assertEqual(deleted_chat_history.user.username, "testuser")
        self.assertEqual(deleted_chat_history.bot.name, "John")
        self.assertEqual(len(deleted_chat_history.history), 1)
        self.assertEqual(deleted_chat_history.input_chars, 10)
        self.assertEqual(deleted_chat_history.level, Decimal("1.0"))

    def test_deletedchathistory_save(self):
        deleted_chat_history = DeletedChatHistory.objects.create(
            user=self.user,
            bot=self.bot,
            history=[{"message": "Hi there!", "timestamp": timezone.now()}],
            input_chars=10,
            level=Decimal("1.0"),
        )
        deleted_chat_history.input_chars = 20
        deleted_chat_history.save()
        self.assertEqual(deleted_chat_history.input_chars, 20)

    def test_level_validation(self):
        with self.assertRaises(ValidationError):
            DeletedChatHistory.objects.create(
                user=self.user,
                bot=self.bot,
                history=[{"message": "Hi there!", "timestamp": timezone.now()}],
                input_chars=10,
                level=Decimal("0.5"),
            )

    def test_input_chars_default(self):
        deleted_chat_history = DeletedChatHistory.objects.create(
            user=self.user,
            bot=self.bot,
            history=[{"message": "Hi there!", "timestamp": timezone.now()}],
            level=Decimal("1.0"),
        )
        self.assertEqual(deleted_chat_history.input_chars, 0)

    def test_deletedchathistory_required_fields(self):
        with self.assertRaises(TypeError):
            DeletedChatHistory.objects.create(
                bot=self.bot,
                history=[{"message": "Hi there!", "timestamp": timezone.now()}],
                input_chars=10,
                level=Decimal("1.0"),
            )


class ChatHistoryModelTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.bot = BotProfile.objects.create(
            name="John",
            gender="M",
            age=30,
            bio="I am a chatbot",
            profession="Chatbot",
            hobbies={"Reading": 8, "Dancing": 7},
            favorites={"Food": "Pizza", "Movie": "The Godfather"},
            physical_attributes={"Height": "5'11\"", "Weight": "150 lbs"},
            profile_image="images/john.png",
        )

    def test_chathistory_creation(self):
        chat_history = ChatHistory.objects.create(
            user=self.user,
            bot=self.bot,
            history=[{"message": "Hi there!", "timestamp": timezone.now()}],
            input_chars=10,
            level=Decimal("1.0"),
        )
        self.assertEqual(chat_history.user.username, "testuser")
        self.assertEqual(chat_history.bot.name, "John")
        self.assertEqual(len(chat_history.history), 1)
        self.assertEqual(chat_history.input_chars, 10)
        self.assertEqual(chat_history.level, Decimal("1.0"))

    def test_level_validation(self):
        with self.assertRaises(ValidationError):
            ChatHistory.objects.create(
                user=self.user,
                bot=self.bot,
                history=[{"message": "Hi there!", "timestamp": timezone.now()}],
                input_chars=10,
                level=Decimal("0.5"),
            )

    def test_chathistory_save(self):
        chat_history = ChatHistory.objects.create(
            user=self.user,
            bot=self.bot,
            history=[{"message": "Hi there!", "timestamp": timezone.now()}],
            input_chars=10,
            level=Decimal("1.0"),
        )
        chat_history.input_chars = 20
        chat_history.save()
        self.assertEqual(chat_history.input_chars, 20)


class UserProfileModelTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="testuser", password="testpass")

    def test_userprofile_creation(self):
        user_profile = UserProfile.objects.create(
            user=self.user,
            age=30,
            gender="M",
            gender_focus="F",
            timezone="Asia/Kolkata",
            experience=5,
            interests="Reading, Dancing, Music",
            is_active=True,
            is_staff=False,
        )
        self.assertEqual(user_profile.user.username, "testuser")
        self.assertEqual(user_profile.age, 30)
        self.assertEqual(user_profile.gender, "M")
        self.assertEqual(user_profile.gender_focus, "F")
        self.assertEqual(user_profile.timezone, "Asia/Kolkata")
        self.assertEqual(user_profile.experience, 5)
        self.assertEqual(user_profile.interests, "Reading, Dancing, Music")
        self.assertTrue(user_profile.is_active)
        self.assertFalse(user_profile.is_staff)

    def test_age_validation(self):
        with self.assertRaises(ValidationError):
            UserProfile.objects.create(
                user=self.user,
                age=10,
                gender="M",
                gender_focus="F",
                timezone="Asia/Kolkata",
                experience=5,
                interests="Reading, Dancing, Music",
                is_active=True,
                is_staff=False,
            )

    def test_gender_validation(self):
        with self.assertRaises(ValidationError):
            UserProfile.objects.create(
                user=self.user,
                age=30,
                gender="X",
                gender_focus="F",
                timezone="Asia/Kolkata",
                experience=5,
                interests="Reading, Dancing, Music",
                is_active=True,
                is_staff=False,
            )

    def test_level_validation(self):
        with self.assertRaises(ValidationError):
            user_profile = UserProfile.objects.create(
                user=self.user,
                age=30,
                gender="M",
                gender_focus="F",
                timezone="Asia/Kolkata",
                experience=5,
                interests="Reading, Dancing, Music",
                is_active=True,
                is_staff=False,
            )
            user_profile.level = Decimal("0.5")
            user_profile.save()

    def test_interests_validation(self):
        with self.assertRaises(ValidationError):
            UserProfile.objects.create(
                user=self.user,
                age=30,
                gender="M",
                gender_focus="F",
                timezone="Asia/Kolkata",
                experience=5,
                interests="Reading, , Music",
                is_active=True,
                is_staff=False,
            )

    def test_timezone_validation(self):
        with self.assertRaises(ValidationError):
            UserProfile.objects.create(
                user=self.user,
                age=30,
                gender="M",
                gender_focus="F",
                timezone="America/NYC",
                experience=5,
                interests="Reading, Dancing, Music",
                is_active=True,
                is_staff=False,
            )

    def test_userprofile_save(self):
        user_profile = UserProfile.objects.create(
            user=self.user,
            age=30,
            gender="M",
            gender_focus="F",
            timezone="Asia/Kolkata",
            experience=5,
            interests="Reading, Dancing, Music",
            is_active=True,
            is_staff=False,
        )
        user_profile.is_staff = True
        user_profile.save()
        self.assertTrue(user_profile.is_staff)
