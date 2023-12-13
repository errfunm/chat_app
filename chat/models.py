from django.db import models
from accounts.models import User


class Participants(models.Model):
    users = models.ManyToManyField(User, related_name='chats')
    date_created = models.DateTimeField(auto_now_add=True)
    is_private = models.BooleanField(default=True)

    def get_other_user(self, current_user):
        return self.users.exclude(id=current_user.id).first().username

    class Meta:
        verbose_name_plural = "Participants"


class PrivateChat(Participants):
    pass


class GroupChat(Participants):
    name = models.CharField(max_length=100)
    is_private = False


class Message(models.Model):
    MESSAGE_CONTENT_TYPES = [
        ('txt', 'Text'),
        ('img', 'Image'),
        ('file', 'File')
    ]

    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    conversation = models.ForeignKey(Participants, on_delete=models.CASCADE, related_name='messages')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    content_type = models.CharField(
        choices=MESSAGE_CONTENT_TYPES,
        max_length=5
    )

    def clear_for_user(self, user):
        # Mark the message as not visible for the specified user
        MessageVisibility.objects.filter(message=self, user=user, is_visible=True).update(is_visible=False)


class TextMessage(Message):
    content = models.TextField()
    content_type = 'txt'

    def save(self, *args, **kwargs):
        if self.pk is None:
            super(TextMessage, self).save()
            for user in self.conversation.users.all():
                MessageVisibility.objects.create(user=user, message=self)

        super(TextMessage, self).save()


class ImageMessage(Message):
    content_type = 'img'
    content = models.ImageField(upload_to='images/')

    def save(self, *args, **kwargs):
        if self.pk is None:
            super(ImageMessage, self).save()
            for user in self.conversation.users.all():
                MessageVisibility.objects.create(user=user, message=self)

        super(ImageMessage, self).save()


class MessageVisibility(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_visible = models.BooleanField(default=True)

    class Meta:
        unique_together = ['message', 'user']


