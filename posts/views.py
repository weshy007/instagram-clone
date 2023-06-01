from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from authentication.models import Profile
from comments.forms import NewCommentForm
from comments.models import Comment

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
        'users_paginator': users_paginator,
    }

    return render(request, 'index.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post).order_by('-date')

    if request.method == 'POST':
        form = NewCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return HttpResponseRedirect(reverse('post-details', args=[post.id]))
    else:
        form = NewCommentForm()

        context = {
            'post': post,
            'form': form,
            'comments': comments
        }

        return render(request, 'post_detail.html', context)


@login_required
def tags(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.objects.filter(tags=tags).order_by('-posted')

    context = {
        'posts': posts,
        'tag': tag
    }

    return render(request, 'tag.html', context)


@login_required
def like(request, post_id):
    post = Post.objects.get(id=post_id)
    liked = Likes.objects.filter(user=request.user, post=post).count()

    if not liked:
        Likes.objects.create(user=request.user, post=post)
        post.likes += 1
    else:
        Likes.objects.filter(user=request.user, post=post).delete()
        post.likes -= 1

    post.save()
    return HttpResponseRedirect(reverse('post-details', args=[post_id]))


@login_required
def favourite(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    profile = get_object_or_404(Profile, user=request.user)

    if post in profile.favourite.all():
        profile.favourite.remove(post)
    else:
        profile.favourite.add(post)

    return HttpResponseRedirect(reverse('post-details', args=[post_id]))
