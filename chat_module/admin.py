from django.contrib import admin
from .models import UserProfile, ChatHistory, DeletedChatHistory

admin.site.register(UserProfile)
admin.site.register(ChatHistory)
admin.site.register(DeletedChatHistory)