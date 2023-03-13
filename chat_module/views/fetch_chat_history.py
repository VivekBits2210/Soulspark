from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework.decorators import api_view

from ai_profiles.models import BotProfile
from chat_module.models import UserProfile, ChatHistory


@login_required
@api_view(['GET'])
def fetch_chat_history(request):
    user = request.user
    lines = int(request.GET.get('lines', 10))
    bot_id = int(request.GET.get('bot_id'))
    bot = None
    if bot_id:
        bot_queryset = BotProfile.objects.filter(bot_id=bot_id)
        if not bot_queryset.exists():
            return JsonResponse({'error': f"bot {bot_id} does not exist."})
        bot = bot_queryset.first()
        chat_history_queryset = ChatHistory.objects.filter(user=user, bot=bot)
    else:
        chat_history_queryset = ChatHistory.objects.filter(user=user)

    if not chat_history_queryset.exists():
        history = []
        if bot_id:
            UserProfile.objects.create(user=user, bot=bot, history=history).save()
    elif lines == 0:
        history = []
    else:
        history = chat_history_queryset.first()[-lines:]
    return JsonResponse({'bot_id': bot_id, 'history': history})