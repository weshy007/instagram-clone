from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
# TODO: from authentication.models import Profile
from django.urls import resolve, reverse

from comments.forms import NewCommentForm
from comments.models import Comment
from authentication.models import Profile

from .forms import NewPostForm
from .models import Follow, Likes, Post, Stream, Tag


# Create your views here.
@login_required
def index(request):
    user = request.user
    follow_status = Follow.objects.filter(following=user, follower=user).exists()

    profile = Profile.objects.all()
    posts = Stream.objects.filter(user=user).values_list('post_id', flat=True)

    post_items = Post.objects.filter(id__in=posts).order_by('-posted')

    query = request.GET.get('q')
    users_paginator = None


    if query:
        users = User.objects.filter(Q(username__icontains=query))
        paginator = Paginator(users, 6)
        page_number = request.GET.get('page')
        users_paginator = paginator.get_page(page_number)

    context = {
        'post_items': post_items,
        'follow_status': follow_status,
        'profile': profile,
        'users_pagnator': users_paginator,
}
        
    return render(request, 'index.html', context)