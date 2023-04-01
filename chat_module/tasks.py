# TODO: Integrate Celery

from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer
from django.utils import timezone

from ai_profiles.models import BotProfile
from chat_module.models import ChatHistory
from dialog_engine.engine import DialogEngine
from user_profiles.models import UserProfile, User

channel_layer = get_channel_layer()


# TODO: Integrate with the Dialog Engine
def get_response(channel_name, input_data):
    email = input_data["email"]
    bot_id = input_data["bot_id"]

    # canned_response = "This is a canned bot response."

    # response = canned_response
    user = User.objects.get(email=email)

    try:
        user_profile = UserProfile.objects.get(user=user)
    except (KeyError, UserProfile.DoesNotExist):
        user_profile = UserProfile.objects.create(user=user)

    bot = BotProfile.objects.get(bot_id=bot_id)
    try:
        chat_history_obj = ChatHistory.objects.get(user=user_profile.user, bot=bot)
    except (KeyError, ChatHistory.DoesNotExist):
        chat_history_obj = ChatHistory.objects.create(
            user=user_profile.user, bot=bot, history=[]
        )

    response = DialogEngine(user_profile, chat_history_obj)
    response = response.run()

    timestamp = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
    packet = {
        "type": "chat_message",
        # "text": {"msg": response, "source": "bot"},
        "source": "bot",
        "who": bot_id,
        "message": response,
        "timestamp": timestamp,
    }
    async_to_sync(channel_layer.send)(
        channel_name,
        packet,
    )

    chat_history_obj.history.append(
        {
            "who": packet["who"],
            "message": packet["message"],
            "timestamp": packet["timestamp"],
        }
    )
    chat_history_obj.save()


@shared_task
def test_celery(data):
    print(data)
