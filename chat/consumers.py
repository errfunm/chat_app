import json
import base64
from django.core.files.base import ContentFile
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.core.serializers import serialize
from .models import TextMessage, ImageMessage, Participants


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
        message_type = text_data_json["message_type"]
        conversation = Participants.objects.get(id=self.room_id)
        message = None
        if message_type == 'text':
            message = text_data_json["message"]
            TextMessage.objects.create(content=message, conversation=conversation,
                                       sender=self.user, content_type='txt')
        elif message_type == 'image':
            image_data = text_data_json["image_data"]
            image_content = base64.b64decode(image_data)
            img_msg = ImageMessage(conversation=conversation, sender=self.user,)
            img_msg.content.save('uploaded_img.jpg', ContentFile(image_content))
            message = self.serialize_image(img_msg)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message", "message": message, 'sender': self.user.username,
                                   'message_type': message_type}
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]
        sender = event["sender"]
        content_type = event["message_type"]
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            "message": message,
            "sender": sender,
            "content_type": content_type
        }))

    def serialize_image(self, image_instance):
        serialized_data = serialize('json', [image_instance])
        deserialized_data = json.loads(serialized_data)
        serialized_image_data = '/' + deserialized_data[0]['fields']["content"]

        return serialized_image_data
