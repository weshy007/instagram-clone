from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from direct_messages.models import Message
from authentication.models import Profile


# Create your views here.
@login_required
def inbox(request):
    user = request.user
    messages = Message.get_message(user)
    active_direct = None
    profile = get_object_or_404(Profile, user=user) 

    if messages:
        message = messages[0]
        active_direct = message['user'].username
        Message.objects.filter(user=user, recipient=message['user']).update(is_read=True)

        for message in messages:
            if message['user'].username == active_direct:
                message['unread'] = 0

    context = {
        'directs': directs,
        'messages': messages,
        'active_direct': active_direct,
        'profile': profile
    }

    return render(request, 'direct/direct.html', context)


def directs(request, username):
    user = request.user
    messages = Message.get_message(user=user)
    active_direct = username
    directs = Message.objects.filter(user=user, recipient__username=username)
    directs.update(is_read = True)

    for message in messages:
        if message['user'].username ==username:
            message['unread'] = 0

    context = {
        'directs': directs,
        'messages': messages,
        'active_direct': active_direct
    }

    return render(request, 'directs/direct.html', context)


def send_directs(request):
    pass


def user_search(request):
    pass


def new_conversation(request):
    pass