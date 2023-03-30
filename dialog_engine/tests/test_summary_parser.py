from rest_framework.test import APITestCase
from chat_module.models import ChatHistory
from chat_module.tests.utils import create_bot, create_user_and_profile
from dialog_engine.tasks import parse_summary


class TestParseSummary(APITestCase):
    def setUp(self):
        self.user, self.encrypted_email, self.user_profile = create_user_and_profile()
        self.bot = create_bot()
        self.raw_summary = (
            "Vivek summary:\n"
            "1. Vivek likes chicken sandwiches\n"
            "2. Vivek hates not having chicken sandwiches\n"
            "Carla summary:\n"
            "3. Carla is a Lovecraftian nightmare brought forth from silicon and matrix math\n"
            "4. Carla also likes chicken sandwiches"
        )

        self.parsed_output = {
            "user": [
                "Vivek likes chicken sandwiches",
                "Vivek hates not having chicken sandwiches",
            ],
            "bot": [
                "Carla is a Lovecraftian nightmare brought forth from silicon and matrix math",
                "Carla also likes chicken sandwiches",
            ],
        }
        self.chat_history_record = ChatHistory(
            user=self.user,
            bot=self.bot,
            history=[],
            user_summary=self.parsed_output["user"],
            bot_summary=self.parsed_output["bot"],
        )

    def test_parse_summary(self):
        test_summary = "summary:\n1. Line 1\n2. Line 2\nsummary:\n3. Line 3\n4. Line 4"
        expected_output = {"user": ["Line 1", "Line 2"], "bot": ["Line 3", "Line 4"]}
        parsed_summary = parse_summary(test_summary)
        self.assertEqual(parsed_summary, expected_output)
        self.chat_history_record.user_summary.extend(parsed_summary["user"])
        self.chat_history_record.bot_summary.extend(parsed_summary["bot"])
        self.chat_history_record.save()
        self.parsed_output["user"].extend(expected_output["user"])
        self.parsed_output["bot"].extend(expected_output["bot"])
        self.assertEqual(
            self.chat_history_record.user_summary, self.parsed_output["user"]
        )
        self.assertEqual(
            self.chat_history_record.bot_summary, self.parsed_output["bot"]
        )

    def test_parse_summary_plain(self):
        test_summary = "1. Line 1\n2. Line 2\n3. Line 3\n4. Line 4"
        expected_output = {"default": ["Line 1", "Line 2", "Line 3", "Line 4"]}
        parsed_summary = parse_summary(test_summary)
        self.assertEqual(parsed_summary, expected_output)

    def test_parse_summary_representative_of_real_input(self):
        parsed_summary = parse_summary(self.raw_summary)
        self.assertEqual(parsed_summary, self.parsed_output)
