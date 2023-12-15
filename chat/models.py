from django.db import models
from accounts.models import User


class Participants(models.Model):
    users = models.ManyToManyField(User, related_name='chats')
    date_created = models.DateTimeField(auto_now_add=True)
    is_private = models.BooleanField()

    def get_other_user(self, current_user):
        return self.users.exclude(id=current_user.id).first()

    def __str__(self):
        if self.is_private:
            return f"private_chat, {self.pk}"
        else:
            return f"group_chat, {self.pk}"

    class Meta:
        verbose_name_plural = "Participants"


class PrivateChat(Participants):
    def save(self, *args, **kwargs):
        self.is_private = True
        super(PrivateChat, self).save()


class GroupChat(Participants):
    name = models.CharField(max_length=100)
    group_pic = models.ImageField(upload_to="group_pic/")

    def save(self, *args, **kwargs):
        self.is_private = False
        super(GroupChat, self).save()

    def __str__(self):
        return self.name


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

    def __str__(self):
        if self.content_type == 'txt':
            return f"{self.sender} to {self.conversation.id} - text message"
        else:
            return f"{self.sender} to {self.conversation.id} - file message"

    def clear_for_user(self, user):
        # Mark the message as not visible for the specified user
        MessageVisibility.objects.filter(message=self, user=user, is_visible=True).update(is_visible=False)


class TextMessage(Message):
    content = models.TextField()
    content_type = 'txt'

    def __str__(self):

        return f"{self.sender} to {self.conversation.id} - {self.content_cutter()}"

    def content_cutter(self):
        string = self.content
        if len(string) > 5:
            return f"'{string[:5]} ...'"
        else:
            return f"'{string[:5]}'"

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

    def __str__(self):
        visibility_status = "Visible" if self.is_visible == True else "Not visible"

        return f"Message: {self.message}, User: {self.user}, Status: {visibility_status}"

    class Meta:
        unique_together = ['message', 'user']


