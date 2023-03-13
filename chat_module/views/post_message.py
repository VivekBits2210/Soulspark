from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
import json

from ai_profiles.models import BotProfile
from chat_module.models import ChatHistory


@login_required
@csrf_exempt
@api_view(['POST'])
def post_message(request):
    user = request.user
    data = json.loads(request.body.decode('utf-8'))
    message = data['message']

    bot_id = data['bot_id']
    bot_id = int(bot_id)
    bot = BotProfile.objects.get(bot_id=bot_id)

    chat_history = ChatHistory.objects.get(user=user, bot=bot)

    # Retrieve the current chat history as a list
    history_list = chat_history.history

    # Add a new message to the history list with a timestamp
    timestamp = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
    history_list.append({
        'from': 'user',
        'timestamp': timestamp,
        'message': message
    })
    chat_history.history = history_list
    chat_history.save()

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.send)('chatbot',
                                      {
                                          "type": "chat_message",
                                          "text": {
                                          "username": user.username,
                                          "bot_id": data['bot_id'],
                                          "message": message
                                          }
                                      })

    return JsonResponse({'status': 'ok'})
