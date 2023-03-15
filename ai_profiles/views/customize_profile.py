from copy import deepcopy
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view

from ai_profiles.models import BotProfile
from chat_module.models import ChatHistory


@login_required()
@api_view(["POST"])
def customize_profile(request):
    request_dict = request.data
    if "bot_id" not in request_dict:
        return JsonResponse(
            {"error": f"No bot_id given"}, status=status.HTTP_400_BAD_REQUEST
        )

    bot_id = request_dict["bot_id"]
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
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Update original bot info with custom info
    original_bot = bot_queryset.first()
    original_dict = model_to_dict(original_bot)
    original_dict.update(request_dict)
    del original_dict["bot_id"]

    # Create bot and a corresponding chat history entry with user
    try:
        bot = BotProfile.objects.create(**original_dict)

        previous_history = {}
        query_set = ChatHistory.objects.filter(user=request.user, bot=original_bot)
        if query_set.exists():
            previous_history = query_set.first().history

        ChatHistory.objects.create(user=request.user, bot=bot, history=previous_history)
    except (ValidationError, TypeError) as e:
        return JsonResponse(repr(e), status=status.HTTP_400_BAD_REQUEST, safe=False)

    return JsonResponse({"bot_id": bot.bot_id}, status=status.HTTP_200_OK)
