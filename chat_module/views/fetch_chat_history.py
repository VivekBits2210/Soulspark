from django.core.exceptions import ValidationError
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view

from ai_profiles.models import BotProfile
from chat_module.models import ChatHistory
from user_profiles.utils import fetch_user_or_error


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
    bot = None
    if bot_id:
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
        if lines == 0:
            return JsonResponse(
                {"bot_id": bot_id, "history": []}, status=status.HTTP_200_OK
            )
    else:
        chat_history_queryset = ChatHistory.objects.filter(user=user)

    if not chat_history_queryset.exists():
        history = []
        if bot_id:
            try:
                history_object = ChatHistory.objects.create(
                    user=user, bot=bot, history=history
                )
            except ValidationError as e:
                return JsonResponse(
                    {"error": repr(e)}, status=status.HTTP_400_BAD_REQUEST
                )
    else:
        history_object = chat_history_queryset.first()
        bot_id = history_object.bot_id

    history = history[-lines:]
    level = history_object.level if history_object else None

    return JsonResponse(
        {"bot_id": bot_id, "history": history, "level": level},
        status=status.HTTP_200_OK,
    )
