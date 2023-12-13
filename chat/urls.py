from django.urls import path
from .views import chat_list, chat_room_view, clear_history

urlpatterns = [
    path('chats/', chat_list, name="chat-view"),
    path('room/<int:pk>', chat_room_view, name="chat-room-view"),
    path('room/<int:pk>/clear-history/', clear_history, name="clear-history")
]
