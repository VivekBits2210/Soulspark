from django.test import SimpleTestCase
from django.urls import reverse, resolve


# from chat_module.views import fetch_user, post_attribute

class ChatModuleUrlsTestCase(SimpleTestCase):
    def test_fetch_user_url_resolves(self):
        url = reverse('fetch-user-info')
        # self.assertEqual(resolve(url).func, fetch_user)

    def test_post_attribute_url_resolves(self):
        url = reverse('post-attribute')
        # self.assertEqual(resolve(url).func, post_attribute)
