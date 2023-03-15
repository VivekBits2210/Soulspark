from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework.decorators import api_view
from ai_profiles.models import BotProfile
from chat_module.models import ChatHistory, DeletedChatHistory


@login_required
@api_view(['POST'])
def unmatch(request):
    user = request.user
    bot_id = request.GET.get('bot_id')
    if not bot_id:
        return JsonResponse({'error': f"No bot_id given"})

    bot_id = int(bot_id)
    bot_queryset = BotProfile.objects.filter(bot_id=bot_id)
    if not bot_queryset.exists():
        return JsonResponse({'error': f"bot {bot_id} does not exist."})

    bot = bot_queryset.first()

    # get all chat history objects for the user and bot
    chat_history_queryset = ChatHistory.objects.filter(user=user, bot=bot)

    # loop through each chat history object and create a corresponding DeletedChatHistory object
    for chat_history_obj in chat_history_queryset:
        DeletedChatHistory.objects.create(user=chat_history_obj.user, bot=chat_history_obj.bot, history=chat_history_obj.history)

    # delete all chat history objects for the user and bot
    chat_history_queryset.delete()

    return JsonResponse({'message': f"All chat history for bot {bot_id} and user {user} moved to DeletedChatHistory"})

