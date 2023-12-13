from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import MessageForm
from .models import Participants, PrivateChat, GroupChat, Message, TextMessage, ImageMessage, MessageVisibility


@login_required()
def chat_list(request):
    current_user = request.user
    chats = Participants.objects.filter(users__username__contains=request.user.username)
    pv_chats = []
    group_chats = []
    for chat in chats:
        if chat.is_private:
            pv_chats.append(PrivateChat.objects.get(id=chat.id))
        else:
            group_chats.append(GroupChat.objects.get(id=chat.id))

        chats = pv_chats + group_chats
    context = {"chats": chats, "current_user": current_user}
    return render(request, 'chat/chat.html', context=context, )


@login_required()
def chat_room_view(request, pk):
    form = MessageForm()
    conversation = Participants.objects.get(id=pk)
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
    conversation = Participants.objects.get(id=pk)
    all_messages = Message.objects.filter(conversation=conversation,)
    print(all_messages)
    for message in all_messages:
        try:
            message.clear_for_user(user=user)
        except MessageVisibility.DoesNotExist:
            pass
    return redirect('chat-room-view', pk=pk)



