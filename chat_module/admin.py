from django.contrib import admin
from chat_module.models import ChatHistory, DeletedChatHistory

admin.site.register(ChatHistory)
admin.site.register(DeletedChatHistory)
