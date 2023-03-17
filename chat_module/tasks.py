from asgiref.sync import async_to_sync
from celery import shared_task
from django.contrib.auth.models import User
from django.utils import timezone
from channels.layers import get_channel_layer

from ai_profiles.models import BotProfile
from chat_module.models import ChatHistory, UserProfile

channel_layer = get_channel_layer()


@shared_task
def get_response(channel_name, input_data):
    username = input_data["username"]
    bot_id = input_data["bot_id"]

    # TODO: Integrate with the Dialog Engine
    canned_response = """
    This is a canned bot response.
    """

    response = canned_response
    timestamp = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
    packet = {
        "type": "chat_message",
        "text": response,
        "username": username,
        "bot_id": bot_id,
        "timestamp": timestamp,
    }
    async_to_sync(channel_layer.send)(
        channel_name,
        packet,
    )

    user = User.objects.get(username=username)
    user_profile = UserProfile.objects.get(user=user)
    bot = BotProfile.objects.get(bot_id=bot_id)
    chat_history_obj = ChatHistory.objects.get(user=user_profile.user, bot=bot)
    chat_history_obj.history.append(packet)
    chat_history_obj.save()
