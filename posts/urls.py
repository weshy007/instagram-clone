from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('newpost', views.new_post, name='newpost'),
    path('<uuid:post_id>', views.post_detail, name='post-details'),
    path('tag/<slug:tag_slug>', views.tags, name='tags'),
    path('<uuid:post_id>/like', views.like, name='like'),
    path('<uuid:post_id>/favourite', views.favourite, name='favourite'),

]