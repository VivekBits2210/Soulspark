from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('fetch-chat-history', views.fetch_chat_history, name='fetch-chat-history'),
    path('post-message', views.post_message, name='post-message'),
]