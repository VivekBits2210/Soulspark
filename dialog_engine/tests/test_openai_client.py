import unittest

import openai.error
from django.core.exceptions import ValidationError
from django.test import TestCase
from dialog_engine.openai_client import GPTClient


class GPTClientTestCase(TestCase):
    def setUp(self):
        self.client = GPTClient()
        self.valid_messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is the capital of France?"},
        ]
        self.valid_customizations = {
            "presence_penalty": 0.5,
            "frequency_penalty": 0.5,
            "temperature": 0.8,
        }

    def test_customize_model_parameters(self):
        self.client.customize_model_parameters(self.valid_customizations)
        for key, value in self.valid_customizations.items():
            self.assertEqual(self.client.parameters[key], value)

    def test_invalid_customization_key(self):
        customizations = {
            "presence_penaltyy": 0.5,
        }
        with self.assertRaises(ValidationError):
            self.client.customize_model_parameters(customizations)

    def test_bad_customization_value(self):
        customizations = {
            "presence_penalty": None,
        }
        with self.assertRaises(ValidationError):
            self.client.customize_model_parameters(customizations)

    def test_generate_reply(self):
        message, tokens = self.client.generate_reply(self.valid_messages)
        self.assertIsInstance(message, str)
        self.assertIsInstance(tokens, int)
        self.assertTrue(tokens >= 0)

    def test_generate_reply_with_customization(self):
        self.client.customize_model_parameters(self.valid_customizations)
        message, tokens = self.client.generate_reply(self.valid_messages)
        self.assertIsInstance(message, str)
        self.assertIsInstance(tokens, int)
        self.assertTrue(tokens >= 0)

    def test_invalid_parameters_returns_invalid_request_error(self):
        # Test for empty messages
        with self.assertRaises(ValidationError):
            self.client.generate_reply([])

        # Test for invalid message format
        with self.assertRaises(ValidationError):
            self.client.generate_reply(
                [
                    {
                        "invalid_key": "system",
                        "content": "You are a helpful assistant.",
                    },
                    {"role": "user", "content": "What is the capital of France?"},
                ]
            )

        # Test for invalid role
        with self.assertRaises(ValidationError):
            self.client.generate_reply(
                [
                    {"role": "invalid_role", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "What is the capital of France?"},
                ]
            )

        # Test for invalid keys
        with self.assertRaises(ValidationError):
            self.client.api_key_list = ["fake-key-1", "fake-key-2"]
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "What is the capital of France?"},
            ]
            response, tokens = self.client.generate_reply(messages)
