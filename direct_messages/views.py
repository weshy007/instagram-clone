from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q
from django.core.paginator import Paginator

from authentication.models import Profile
from direct_messages.models import Message


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
        if message['user'].username == username:
            message['unread'] = 0

    context = {
        'directs': directs,
        'messages': messages,
        'active_direct': active_direct
    }

    return render(request, 'directs/direct.html', context)


def send_directs(request):
    if request.method == 'POST':
        from_user = request.user
        to_user_username = request.POST.get('to_user')
        body = request.POST.get('body')

        to_user = get_object_or_404(User, username=to_user_username)
        Message.sender_message(from_user, to_user, body)
        
    return redirect('message')


def user_search(request):
    query = request.GET.get('q')
    context = {}

    if query:
        users = User.objects.filter(username__icontains=query)

        #Paginator
        paginator = Paginator(users, 8)
        page_number = request.GET.get('page')
        users_paginator = paginator.get_page(page_number)

        context = {
            'users': users_paginator
        }
    
    return render(request, 'directs/search.html', context)


def new_conversation(request, username):
    from_user = request.user
    
    try:
        to_user = get_object_or_404(User, username=username)
    except User.DoesNotExist:
        return redirect('search-users')
    
    if from_user != to_user:
        Message.sender_message(from_user, to_user, '')
    return redirect('message')