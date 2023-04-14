from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view

from ai_profiles.models import BotProfile
from chat_module.models import ChatHistory
from user_profiles.utils import fetch_user_or_error


@api_view(["GET"])
def fetch_level(request):
    user_or_error = fetch_user_or_error(request)
    if isinstance(user_or_error, JsonResponse):
        error_response = user_or_error
        return error_response
    user = user_or_error

    bot_id = request.GET.get("bot_id")
    if not bot_id:
        return JsonResponse(
            {"error": f"bot ID is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        bot_id = int(bot_id)
    except ValueError:
        return JsonResponse(
            {"error": f"Bot ID {bot_id} is not an integer."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    bot_queryset = BotProfile.objects.filter(bot_id=bot_id)
    if not bot_queryset.exists():
        return JsonResponse(
            {"error": f"bot {bot_id} does not exist."},
            status=status.HTTP_404_NOT_FOUND,
        )

    bot = bot_queryset.first()
    chat_history_queryset = ChatHistory.objects.filter(user=user, bot=bot)
    if not chat_history_queryset.exists():
        return JsonResponse(
            {"error": f"Bot {bot} does not have chat history with this user."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    level = chat_history_queryset.first().level
    return JsonResponse(
        {"level": level},
        status=status.HTTP_200_OK,
    )
