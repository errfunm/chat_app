from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import MessageForm
from .models import PrivateChat, Message, TextMessage, ImageMessage, MessageVisibility


@login_required()
def chat_room_view(request):
    chats = PrivateChat.objects.filter(users__username__contains=request.user.username)
    context = {"chats": chats}
    return render(request, 'chat/chat.html', context=context, )


@login_required()
def message_view(request, pk):
    form = MessageForm()
    conversation = PrivateChat.objects.get(id=pk)
    all_messages = Message.objects.filter(conversation=conversation,)
    visible_messages = []
    for message in all_messages:
        if MessageVisibility.objects.filter(message=message, user=request.user, is_visible=True):
            if message.content_type == 'txt':
                message = TextMessage.objects.get(id=message.id)
                visible_messages.append(message)
            if message.content_type == 'img':
                message = ImageMessage.objects.get(id=message.id)
                visible_messages.append(message)
            if message.content_type == 'file':
                pass

    return render(request, 'chat/messages.html', context={"id": pk, "form": form, "messages": visible_messages})


@login_required()
def clear_history(request, pk):
    user = request.user
    conversation = PrivateChat.objects.get(id=pk)
    all_messages = Message.objects.filter(conversation=conversation,)
    print(all_messages)
    for message in all_messages:
        try:
            message.clear_for_user(user=user)
        except MessageVisibility.DoesNotExist:
            pass
    return redirect('chat-room-view', pk=pk)



