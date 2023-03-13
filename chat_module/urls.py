from django.urls import path
from chat_module.views import index, fetch_chat_history, post_message, unmatch

urlpatterns = [
    path('', index.index, name='index'),
    path('fetch-chat-history', fetch_chat_history.fetch_chat_history, name='fetch-chat-history'),
    path('post-message', post_message.post_message, name='post-message'),
    path('unmatch', unmatch.unmatch, name='unmatch')
]