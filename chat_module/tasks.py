# TODO: Integrate Celery

from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer
from django.utils import timezone

from dialog_engine.engine import DialogEngine
import logging

logger = logging.getLogger("my_logger")
channel_layer = get_channel_layer()


def get_response(channel_name, user, user_profile, bot, chat_history_obj):
    engine = DialogEngine(user_profile, chat_history_obj)
    response = engine.run()

    timestamp = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
    packet = {
        "type": "chat_message",
        "source": "bot",
        "who": bot.bot_profile_id,
        "message": response,
        "timestamp": timestamp,
    }
    logger.info(f"Packet from bot: {packet}")

    async_to_sync(channel_layer.send)(
        channel_name,
        packet,
    )

    logger.info("Now appending bot message to chat history")
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
