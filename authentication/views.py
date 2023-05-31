from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import resolve, reverse

from comments.forms import NewCommentForm
from comments.models import Comment
from posts.forms import NewPostForm
from posts.models import Follow, Likes, Post, Stream, Tag

from .forms import EditProfileForm, UserRegisterForm
from .models import Profile


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            new_user = form.save()
            messages.success(request, f'Hurray, your account was created!!')

            # Auto Login
            new_user = authenticate(username=username,password=password)
            login(request, new_user)

            return redirect('index')
        else:
        # Handle form validation errors
            error_messages = form.errors.get_json_data(escape_html=False)
            for field, errors in error_messages.items():
                for error in errors:
                    messages.error(request, f"Error in field '{field}': {error['message']}")

    elif request.user.is_authenticated:
        return redirect('index')
    else:
        form = UserRegisterForm()
    context = {
        'form': form,
    }
    return render(request, 'sign_up.html', context)



def user_profile(request, username):
    Profile.objects.get_or_create(user=request.user)
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=user)
    url_name = resolve(request.path).url_name
    posts = Post.objects.filter(user=user).order_by('-posted')

    if url_name == 'profile':
        posts = Post.objects.filter(user=user).order_by('posted')
    else:
        posts = profile.favourite.all()

    # Profile statistics
    posts_count = Post.objects.filter(user=user).count()
    following_count = Follow.objects.filter(follower=user).count()
    followers_count = Follow.objects.filter(following=user).count()
    follow_status = Follow.objects.filter(following=user, follower=request.user).exists()

    # Pagination's
    paginator = Paginator(posts, 8)
    page_number = request.GET.get('page')
    posts_paginator = paginator.get_page(page_number)

    context = {
        'posts': posts,
        'profile': profile,
        'posts_count': posts_count,
        'following_count': following_count,
        'followers_count': followers_count,
        'posts_paginator': posts_paginator,
        'follow_status': follow_status,
    }

    return render(request, 'profile.html', context)


def edit_profile(request):
    user = request.user.id
    profile = Profile.objects.get(user__id=user)

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if form.is_valid():
            profile.image = form.cleaned_data.get('image')
            profile.first_name = form.cleaned_data.get('first_name')
            profile.last_name = form.cleaned_data.get('last_name')
            profile.location = form.cleaned_data.get('location')
            profile.url = form.cleaned_data.get('url')
            profile.bio = form.cleaned_data.get('bio')
            profile.save()

            return redirect('profile', profile.user.username)
        else:
            form = EditProfileForm(instance=request.user.profile)

        context = {
            'form': form,
        }

        return render(request, 'edit_profile.html', context)


def follow(request):
    pass
