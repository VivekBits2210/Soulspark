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
    bot_data_list = (
        ChatHistory.objects.filter(user=user)
        .values("bot__bot_profile_id", "bot__name", "level")
        .distinct()
        .order_by("-level")
    )
    response_data = [
        {"name": bot_data["bot__name"], "bot_profile_id": bot_data["bot__bot_profile_id"]}
        for bot_data in bot_data_list
    ]
    return JsonResponse({"data": response_data}, status=status.HTTP_200_OK)
