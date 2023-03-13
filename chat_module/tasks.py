from asgiref.sync import async_to_sync
from celery import shared_task
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
    async_to_sync(channel_layer.send)(
        channel_name,
        {
            "type": "chat.message",
            "text": {"message": response,
                     "username": None,
                     },
        },
    )
