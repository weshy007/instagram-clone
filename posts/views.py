from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# TODO: from comment.models import Comment
# TODO: from comment.forms import NewCommentForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
# TODO: from authentication.models import Profile
from django.urls import resolve, reverse

from .forms import NewPostForm
from .models import Follow, Likes, Post, Stream, Tag


# Create your views here.