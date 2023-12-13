from django.contrib import admin
from .models import *


class PrivateChatAdmin(admin.ModelAdmin):
    filter_horizontal = ('users',)


admin.site.register(Participants)
admin.site.register(PrivateChat, PrivateChatAdmin)
admin.site.register(Message)
admin.site.register(TextMessage)
admin.site.register(ImageMessage)
admin.site.register(MessageVisibility)
admin.site.register(GroupChat)
