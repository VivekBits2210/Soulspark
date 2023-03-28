from django.core.exceptions import ValidationError
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view

from ai_profiles.models import BotProfile
from chat_module.models import ChatHistory
from user_profiles.models import User
from user_profiles.utils import decrypt_email


@api_view(["GET"])
def fetch_chat_history(request):
    encrypted_email = request.GET.get('email')
    email = decrypt_email(encrypted_email)

    try:
        user = User.objects.get(pk=email)
    except User.DoesNotExist:
        error_message = {'error': f'User {encrypted_email} not found'}
        return JsonResponse(error_message, status=status.HTTP_404_NOT_FOUND)

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
                ChatHistory.objects.create(user=user, bot=bot, history=history)
            except ValidationError as e:
                return JsonResponse(repr(e), status=status.HTTP_400_BAD_REQUEST)
    else:
        history_object = chat_history_queryset.first()
        bot_id = history_object.bot_id
        history = history_object.history[-lines:]

    return JsonResponse(
        {"bot_id": bot_id, "history": history}, status=status.HTTP_200_OK
    )
