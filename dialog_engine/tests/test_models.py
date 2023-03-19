from django.test import TestCase
from chat_module.tests.utils import create_user_and_profile, create_bot
from dialog_engine.models import GPTUsageRecord


class GPTUsageRecordModelTestCase(TestCase):
    def setUp(self):
        self.user, self.user_profile = create_user_and_profile()
        self.bot = create_bot()
        self.gpt_usage_record_data = {
            "user": self.user,
            "bot": self.bot,
            "indicator_tokens": 10,
            "story_tokens": 20,
            "indicator_vector": "0.1,0.2,0.3",
            "indicator_version": "1.0",
            "chat_history_length": 50,
        }

    def test_create_gpt_usage_record(self):
        gpt_usage_record = GPTUsageRecord.objects.create(**self.gpt_usage_record_data)
        self.assertEqual(gpt_usage_record.user, self.user)
        self.assertEqual(gpt_usage_record.bot, self.bot)
        self.assertEqual(gpt_usage_record.indicator_tokens, 10)
        self.assertEqual(gpt_usage_record.story_tokens, 20)
        self.assertEqual(gpt_usage_record.summarizer_tokens, 0)
        self.assertEqual(gpt_usage_record.indicator_vector, "0.1,0.2,0.3")
        self.assertEqual(gpt_usage_record.indicator_version, "1.0")
        self.assertEqual(gpt_usage_record.chat_history_length, 50)

    def test_unique_together_constraint(self):
        GPTUsageRecord.objects.create(**self.gpt_usage_record_data)
        with self.assertRaises(Exception):
            GPTUsageRecord.objects.create(**self.gpt_usage_record_data)

    def test_required_fields(self):
        for field in GPTUsageRecord.REQUIRED_FIELDS:
            with self.subTest(field=field):
                data = self.gpt_usage_record_data.copy()
                del data[field]
                with self.assertRaises(Exception):
                    GPTUsageRecord.objects.create(**data)

    def test_str_representation(self):
        gpt_usage_record = GPTUsageRecord.objects.create(**self.gpt_usage_record_data)
        expected_str = (
            f"GPTUsageRecord({self.user.username}, {self.bot.name}, indicator_tokens={10}, "
            f"story_tokens={20}, summarizer_tokens={0}, "
            f"indicator_vector=0.1,0.2,0.3, indicator_version={1.0}, "
            f"chat_history_length={50})"
        )
        self.assertEqual(str(gpt_usage_record), expected_str)
