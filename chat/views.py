from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import TextMessageForm
from .models import PrivateChat, TextMessage, MessageVisibility


@login_required()
def chat_room_view(request):
    chats = PrivateChat.objects.filter(users__username__contains=request.user.username)
    context = {"chats": chats}
    return render(request, 'chat/chat.html', context=context, )


@login_required()
def message_view(request, pk):
    form = TextMessageForm()
    conversation = PrivateChat.objects.get(id=pk)
    all_messages = TextMessage.objects.filter(conversation=conversation,)
    visible_messages = []
    for message in all_messages:
        if MessageVisibility.objects.filter(message=message, user=request.user, is_visible=True):
            visible_messages.append(message)

    return render(request, 'chat/messages.html', context={"id": pk, "form": form, "messages": visible_messages})


@login_required()
def clear_history(request, pk):
    user = request.user
    conversation = PrivateChat.objects.get(id=pk)
    all_messages = TextMessage.objects.filter(conversation=conversation,)
    print(all_messages)
    for message in all_messages:
        try:
            message.clear_for_user(user=user)
        except MessageVisibility.DoesNotExist:
            pass
    return redirect('chat-room-view', pk=pk)



