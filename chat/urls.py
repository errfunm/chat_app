from django.urls import path
from .views import chat_room_view, message_view, clear_history

urlpatterns = [
    path('', chat_room_view, name="chat-view"),
    path('messaging/<int:pk>', message_view, name="chat-room-view"),
    path('messaging/<int:pk>/clear-history/', clear_history, name="clear-history")
]
