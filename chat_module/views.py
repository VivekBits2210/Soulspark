# Create your views here.
import json
from django.views.decorators.csrf import csrf_exempt
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view

from ai_profiles.models import BotProfile
from .models import UserProfile, ChatHistory


@api_view(['GET'])
def index(request):
    return HttpResponse("You are at the chat module index.")


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
        history = {}
        if bot_id:
            UserProfile.objects.create(user=user, bot=bot, history=history).save()
    elif lines == 0:
        history = {}
    else:
        history = chat_history_queryset.first()[-lines:]
    return JsonResponse({'bot_id': bot_id, 'history': history})


# TODO: call this api when unmatching
@login_required
@api_view(['POST'])
def delete_bot_mapping(request):
    pass


@login_required
@csrf_exempt
@api_view(['POST'])
def post_message(request):
    user = request.user
    data = json.loads(request.body.decode('utf-8'))
    message = data['message']
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.send)('chatbot',
                                      {
                                          "type": "chat_message",
                                          "username": user.username,
                                          "bot_id": data['bot_id'],
                                          "message": message
                                      })

    return JsonResponse({'status': 'ok'})
