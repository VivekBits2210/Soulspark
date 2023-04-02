from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view

from chat_module.models import ChatHistory
from user_profiles.utils import fetch_user_or_error


@api_view(["GET"])
def fetch_selected_profiles(request):
    user_or_error = fetch_user_or_error(request)
    if isinstance(user_or_error, JsonResponse):
        error_response = user_or_error
        return error_response
    user = user_or_error
    bot_id_list = list(
        ChatHistory.objects.filter(user=user).values_list("bot", flat=True)
    )
    return JsonResponse({"bot_id_list": bot_id_list}, status=status.HTTP_200_OK)
