from unittest import TestCase
from chat_module.models import ChatHistory
from chat_module.tests.utils import create_bot, create_user_and_profile
from dialog_engine.engine import DialogEngine
from dialog_engine.tasks import parse_summary, summarizer


class TestParseSummary(TestCase):
    def test_parse_summary(self):
        test_summary = "summary:\n1. Line 1\n2. Line 2\nsummary:\n3. Line 3\n4. Line 4"
        expected_output = {
            "user": ["Line 1", "Line 2"],
            "bot": ["Line 3", "Line 4"]
        }
        parsed_summary = parse_summary(test_summary)
        self.assertEqual(parsed_summary, expected_output)

    def test_parse_summary_plain(self):
        test_summary = "1. Line 1\n2. Line 2\n3. Line 3\n4. Line 4"
        expected_output = {
            "default": ["Line 1", "Line 2","Line 3", "Line 4"]
        }
        parsed_summary = parse_summary(test_summary)
        self.assertEqual(parsed_summary, expected_output)

    def test_parse_summary_representative_of_real_input(self):
        pass

    def test_parse_summary_piped_from_chat_history_record(self):
        pass

    def test_parse_summary_invalid_subtle(self):
        pass

    def test_parse_summary_invalid_obvious(self):
        pass


class TestSummarizer(TestCase):

    def setUp(self):
        self.user, self.user_profile = create_user_and_profile()
        self.bot = create_bot()

        # TODO: Create
        self.valid_messages = []
        self.valid_bot_summary = []
        self.valid_user_summary = []
        self.valid_summary_index = 0
        self.chat_history_record = ChatHistory(user=self.user, bot=self.bot, history=self.valid_messages)
        self.dialog_engine = DialogEngine(self.user_profile, self.chat_history_record)

        self.keep_limit = 10
