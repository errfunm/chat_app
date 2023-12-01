from django.urls import path
from .views import chat_room_view, message_view

urlpatterns = [
    path('', chat_room_view, name="chat-view"),
    path('messaging/<int:pk>', message_view, name="start-chat-view")
]
