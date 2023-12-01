from django.db import models
from accounts.models import User


class Participants(models.Model):
    users = models.ManyToManyField(User, related_name='chats')
    date_created = models.DateTimeField(auto_now_add=True)
    is_private = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Participants"


class PrivateChat(Participants):
    pass


class Message(models.Model):
    MESSAGE_CONTENT_TYPES = [
        ('txt', 'Text'),
        ('img', 'Image'),
        ('file', 'File')
    ]

    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    conversation = models.ForeignKey(PrivateChat, on_delete=models.CASCADE, related_name='messages')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    content_type = models.CharField(
        choices=MESSAGE_CONTENT_TYPES,
        max_length=5
    )


class TextMessage(Message):
    text_content = models.TextField()
    content_type = 'txt'
