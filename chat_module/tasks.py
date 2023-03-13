from asgiref.sync import async_to_sync
from django.utils import timezone
from channels.layers import get_channel_layer

channel_layer = get_channel_layer()


# TODO: Make this a shared task once celery is setup
# @shared_task
def get_response(channel_name, input_data):
    # TODO: Integrate with the Dialogue Engine
    canned_response = """
    This is a canned bot response.
    """

    response = canned_response
    timestamp = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
    async_to_sync(channel_layer.send)(
        channel_name,
        {
            "type": "chat_message",
            "text": response,
            "username": None,
            "bot_id": input_data["bot_id"],
            "timestamp": timestamp
        },
    )
