# TODO: Integrate Celery
from celery import shared_task

from asgiref.sync import async_to_sync
from django.contrib.auth.models import User
from django.utils import timezone
from channels.layers import get_channel_layer

from ai_profiles.models import BotProfile
from chat_module.models import ChatHistory
from user_profiles.models import UserProfile

from dialog_engine.engine import DialogEngine

channel_layer = get_channel_layer()


# TODO: Integrate with the Dialog Engine
def get_response(channel_name, input_data):
    username = input_data["username"]
    bot_id = input_data["bot_id"]

    # canned_response = "This is a canned bot response."

    # response = canned_response
    user = User.objects.get(username=username)
    try:
        user_profile = UserProfile.objects.get(user=user)
    except:
        #redirect to userprofile creation?
        pass
    bot = BotProfile.objects.get(bot_id=bot_id)
    chat_history_obj = ChatHistory.objects.get(user=user_profile.user, bot=bot)

    response = DialogEngine(user_profile, chat_history_obj)
    response = response.run()
    print(response)
    timestamp = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
    packet = {
        "type": "chat_message",
        # "text": {"msg": response, "source": "bot"},
        "who": "bot",
        "message": response,
        "username": username,
        "bot_id": bot_id,
        "timestamp": timestamp,
    }
    async_to_sync(channel_layer.send)(
        channel_name,
        packet,
    )

    chat_history_obj.history.append(packet)
    chat_history_obj.save()
