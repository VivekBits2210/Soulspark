import unittest
from unittest.mock import MagicMock
from django.test import TestCase

from chat_module.tests.utils import create_bot, create_user_and_profile
from dialog_engine.components import Components


class ComponentTestcase(TestCase):
    def setUp(self):
        self.user, self.user_profile = create_user_and_profile()
        self.bot = create_bot()
        self.chat_history = []

    @unittest.skip
    def test_construct_conversation_from_chat_history(self):
        components = Components(self.user_profile, self.bot, self.chat_history)
        chat_history = [
            {"source": "User", "message": "Hello"},
            {"source": "Bot", "message": "Hi there"},
        ]
        components.chat_history = chat_history
        expected_conversation = "User: Hello\nBot: Hi there\n"
        self.assertEqual(components.chat_conversation, expected_conversation)

    @unittest.skip
    def test_generate_indicator_prompt(self):
        user_profile = {"name": "Alice"}
        bot = {"name": "Bob"}
        chat_history = []

        components = Components(user_profile, bot, chat_history)
        components.recipe.construct_indicator_system_message = MagicMock(
            return_value=("indicator prompt", {})
        )

        messages, customizations = components.generate_indicator_prompt()

        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0]["role"], "system")
        self.assertEqual(messages[0]["content"], "indicator prompt")
        self.assertEqual(messages[1]["role"], "user")
        self.assertIsNone(messages[1]["content"])

    @unittest.skip
    def test_generate_story_prompt(self):
        user_profile = {"name": "Alice"}
        bot = {"name": "Bob"}
        chat_history = []

        components = Components(user_profile, bot, chat_history)
        components.recipe.construct_story_system_message = MagicMock(
            return_value=("story prompt", {})
        )

        messages, customizations = components.generate_story_prompt()

        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0]["role"], "system")
        self.assertEqual(messages[0]["content"], "story prompt")

    @unittest.skip
    def test_generate_summarization_prompt(self):
        components = Components(self.user_profile, self.bot, self.chat_history)
        messages, customizations = components.generate_summarization_prompt()
        self.assertIsNotNone(messages)
        self.assertIsNotNone(customizations)

    @unittest.skip
    def test_parse_indicator_message(self):
        components = Components(self.user_profile, self.bot, self.chat_history)
        message_text = "sadness:5/10|happiness:3/10|lighthearted:4/10|displeasure:2/10|anger:1/10|confusion:7/10|horny:6/10|disappointment:8/10|boredom:9/10"
        indicator_mapping = components.parse_indicator_message(message_text)
        expected_mapping = {
            "sadness": 5,
            "happiness": 3,
            "lighthearted": 4,
            "displeasure": 2,
            "anger": 1,
            "confusion": 7,
            "horny": 6,
            "disappointment": 8,
            "boredom": 9,
        }
        self.assertEqual(indicator_mapping, expected_mapping)

    @unittest.skip
    def test_find_region(self):
        components = Components(self.user_profile, self.bot, self.chat_history)
        indicator_vector = (5, 3, 4, 2, 1, 7, 6, 8, 9)
        region_index = components.find_region(indicator_vector)
        self.assertIsNotNone(region_index)

    # def test_fetch_template(self):
    #     components = Components(self.user_profile, self.bot, self.chat_history)
    #     region_index = 0
    #     template = components.fetch_template(region_index)
    #     self.assertIsNotNone(template)
