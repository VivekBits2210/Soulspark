from django.core.exceptions import ValidationError
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from ai_profiles.models import BotProfile
from chat_module.models import ChatHistory, DeletedChatHistory
from user_profiles.utils import fetch_user_or_error


@api_view(["POST"])
def unmatch(request):
    user_or_error = fetch_user_or_error(request)
    if isinstance(user_or_error, JsonResponse):
        error_response = user_or_error
        return error_response
    user = user_or_error

    request_dict = request.data
    if "bot_id" not in request_dict:
        return JsonResponse(
            {"error": f"No bot_id given"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        bot_id = int(request_dict["bot_id"])
    except ValueError:
        return JsonResponse(
            {"error": f"Bot ID {request_dict['bot_id']} is not an integer."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    bot_queryset = BotProfile.objects.filter(bot_id=bot_id)
    if not bot_queryset.exists():
        return JsonResponse(
            {"error": f"Bot {bot_id} does not exist."},
            status=status.HTTP_404_NOT_FOUND,
        )

    bot = bot_queryset.first()

    # get all chat history objects for the user and bot
    chat_history_queryset = ChatHistory.objects.filter(user=user, bot=bot)

    # loop through each chat history object and create a corresponding DeletedChatHistory object
    for chat_history_obj in chat_history_queryset:
        try:
            DeletedChatHistory.objects.create(
                email=chat_history_obj.user.email,
                bot_name=chat_history_obj.bot.name,
                history=chat_history_obj.history,
                input_chars=chat_history_obj.input_chars,
                level=chat_history_obj.level,
            )
        except ValidationError as e:
            return JsonResponse({"error": repr(e)}, status=status.HTTP_400_BAD_REQUEST)

    # delete all chat history objects for the user and bot
    chat_history_queryset.delete()

    return JsonResponse(
        {
            "message": f"All chat history for bot {bot_id} and user {user} moved to DeletedChatHistory"
        },
        status=status.HTTP_200_OK,
    )
