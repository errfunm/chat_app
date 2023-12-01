from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import TextMessageForm
from .models import PrivateChat, TextMessage
from accounts.models import User


@login_required()
def chat_room_view(request):
    chats = PrivateChat.objects.filter(users__username__contains=request.user.username)
    context = {"chats": chats}
    return render(request, 'chat/chat.html', context=context, )


@login_required()
def message_view(request, pk):

    conversation = PrivateChat.objects.get(id=pk)
    user = User.objects.get(username=request.user)
    messages = TextMessage.objects.filter(conversation=conversation)

    if request.method == 'POST':
        form = TextMessageForm(request.POST)

        if form.is_valid():
            print("Form is valid!")
            message = form.save(commit=False)
            print("Form not saved yet!")
            message.sender = user
            message.conversation = conversation
            message.save()
            print("Form saved!")
            return redirect('start-chat-view', pk=pk)
    else:
        form = TextMessageForm()

    context = {"messages": messages, "form": form}
    return render(request, "chat/messages.html", context)

