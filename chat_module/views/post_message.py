from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json


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
