import random
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view

from ai_profiles.models import BotProfile
from chat_module.models import ChatHistory
from user_profiles.utils import fetch_user_or_error


def matched():
    return random.random() <= 1


@api_view(["GET"])
def delete_all_chat_history(request):
    user_or_error = fetch_user_or_error(request)
    if isinstance(user_or_error, JsonResponse):
        error_response = user_or_error
        return error_response
    user = user_or_error

    chat_history_queryset = ChatHistory.objects.filter(user=user)
    chat_history_queryset.delete()

    return JsonResponse(
        {"message": f"All chat history for user {user.email} deleted"},
        status=status.HTTP_200_OK,
    )
