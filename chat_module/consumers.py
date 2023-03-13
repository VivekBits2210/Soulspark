import json
from .tasks import get_response
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        get_response.delay(self.channel_name, text_data_json)

        async_to_sync(self.channel_layer.send)(
            self.channel_name,
            {
                "type": "chat_message",
                "text": text_data_json["text"],
                "username": text_data_json["username"],
                "bot_id": text_data_json["bot_id"],
                "timestamp": text_data_json["timestamp"]
            },
        )

    # NOTE: The structure of 'event' is defined by the UI
    def chat_message(self, event):
        packet = json.dumps({
            "type": "chat_message",
            "text": event["text"],
            "username": event["username"],
            "bot_id": event["bot_id"],
            "timestamp": event["timestamp"]
        })
        self.send(text_data=packet)
