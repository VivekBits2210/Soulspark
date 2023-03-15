from django.contrib import admin
from chat_module.models import UserProfile, ChatHistory, DeletedChatHistory

admin.site.register(UserProfile)
admin.site.register(ChatHistory)
admin.site.register(DeletedChatHistory)