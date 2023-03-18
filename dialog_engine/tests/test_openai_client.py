import unittest

import openai.error
from django.test import TestCase
from dialog_engine.openai_client import GPTClient


class GPTClientTestCase(TestCase):
    def setUp(self):
        self.client = GPTClient()

    @unittest.skip
    def test_customize_model_parameters(self):
        customizations = {
            "presence_penalty": 0.5,
            "frequency_penalty": 0.5,
            "temperature": 0.8,
        }
        self.client.customize_model_parameters(customizations)
        for key, value in customizations.items():
            self.assertEqual(self.client.parameters[key], value)

    @unittest.skip
    def test_generate_reply(self):
        client = GPTClient()

        # Test for successful response
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is the capital of France?"},
        ]
        response, _ = client.generate_reply(messages)
        self.assertIsNotNone(response)
        self.assertIn("message", response)
        self.assertIsInstance(response["message"], dict)
        self.assertIn("content", response["message"])

        # Test for empty messages
        with self.assertRaises(openai.error.InvalidRequestError):
            client.generate_reply([])

        # Test for invalid message format
        with self.assertRaises(openai.error.InvalidRequestError):
            client.generate_reply(
                [
                    {
                        "invalid_key": "system",
                        "content": "You are a helpful assistant.",
                    },
                    {"role": "user", "content": "What is the capital of France?"},
                ]
            )

        # Test for invalid role
        with self.assertRaises(openai.error.InvalidRequestError):
            client.generate_reply(
                [
                    {"role": "invalid_role", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "What is the capital of France?"},
                ]
            )
