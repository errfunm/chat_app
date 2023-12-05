import json


from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import TextMessage, PrivateChat

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_name = f"chat_{self.room_id}"
        self.user = self.scope["user"]

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        conversation = PrivateChat.objects.get(id=self.room_id)
        TextMessage.objects.create(text_content=message, conversation=conversation, sender=self.user)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message", "message": message, 'sender': self.user.username}
        )
        # self.send(text_data=json.dumps({"message": message}))

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]
        sender = event["sender"]
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            "message": message,
            "sender": sender
        }))
