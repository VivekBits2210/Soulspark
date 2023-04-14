import random
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view

from chat_module.models import ChatHistory, DeletedChatHistory
from user_profiles.utils import fetch_user_or_error


def matched():
    return random.random() <= 1


@api_view(["POST"])
def delete_all_chat_history(request):
    user_or_error = fetch_user_or_error(request)
    if isinstance(user_or_error, JsonResponse):
        error_response = user_or_error
        return error_response
    user = user_or_error

    chat_history_queryset = ChatHistory.objects.filter(user=user)
    for chat_history_obj in chat_history_queryset:
        DeletedChatHistory.objects.create(
            email=chat_history_obj.user.email,
            bot_name=chat_history_obj.bot.name,
            history=chat_history_obj.history,
            input_chars=chat_history_obj.input_chars,
            level=chat_history_obj.level,
        )

    chat_history_queryset.delete()

    return JsonResponse(
        {"message": f"All chat history for user {user.email} deleted"},
        status=status.HTTP_200_OK,
    )
