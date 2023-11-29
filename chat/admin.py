from django.contrib import admin
from .models import *

admin.site.register(Participants)
admin.site.register(PrivateChat)
admin.site.register(Message)
admin.site.register(TextMessage)
