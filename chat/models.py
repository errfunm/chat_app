from django.db import models
from accounts.models import User


class Participants(models.Model):
    users = models.ManyToManyField(User,)
    date_created = models.DateTimeField(auto_now_add=True)
    is_private = models.BooleanField(default=True)


class PrivateChat(models.Model):
    participants = models.OneToOneField(Participants, on_delete=models.CASCADE)


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    conversation = models.ForeignKey(PrivateChat, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    content_type = models.CharField(max_length=20)


class TextMessage(models.Model):
    message = models.OneToOneField(Message, on_delete=models.CASCADE, primary_key=True)
    text_content = models.TextField()
