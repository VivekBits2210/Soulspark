from django.test import TestCase
from django.urls import reverse
class URLTestCase(TestCase):
    def test_index_url(self):
        url = reverse('chat_module_index')
        self.assertEqual(url, '/chat-module/')

    def test_fetch_chat_history_url(self):
        url = reverse('fetch_chat_history')
        self.assertEqual(url, '/chat-module/fetch-chat-history')

    def test_unmatch_url(self):
        url = reverse('unmatch')
        self.assertEqual(url, '/chat-module/unmatch')
