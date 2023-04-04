import random
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view

from ai_profiles.models import BotProfile
from chat_module.models import ChatHistory
from user_profiles.utils import fetch_user_or_error


def matched():
    return random.random() <= 0.3


@api_view(["GET"])
def fetch_chat_history(request):
    user_or_error = fetch_user_or_error(request)
    if isinstance(user_or_error, JsonResponse):
        error_response = user_or_error
        return error_response
    user = user_or_error

    try:
        lines = int(request.GET.get("lines", 10))
        if lines < 0:
            lines = 10
    except ValueError:
        lines = 10

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
    if lines == 0:
        if matched():
            chat_history_queryset = ChatHistory.objects.filter(user=user)
            if len(chat_history_queryset) == 3:
                return JsonResponse(
                    {"error": "Already matched with 3"}, status=status.HTTP_400_BAD_REQUEST
                )

            chat_history_object = ChatHistory.objects.create(user=user, bot=bot, history=[])
            level = chat_history_object.level
            return JsonResponse(
                {"bot_id": bot_id, "history": [], "level": level}, status=status.HTTP_200_OK
            )
        else:
            return JsonResponse(
                {"bot_id": None, "history": []}, status=status.HTTP_200_OK
            )

    chat_history_queryset = ChatHistory.objects.filter(user=user, bot=bot)
    if not chat_history_queryset.exists():
        return JsonResponse(
            {"error": f"Bot {bot} does not have chat history with this user."}, status=status.HTTP_400_BAD_REQUEST
        )

    history_object = chat_history_queryset.first()
    bot_id = history_object.bot_id
    history = history_object.history[-lines:]
    level = history_object.level if history_object else None

    return JsonResponse(
        {"bot_id": bot_id, "history": history, "level": level},
        status=status.HTTP_200_OK,
    )
