from django.urls import path 
from . import views

urlpatterns = [
    path('', views.inbox, name="message"),
    path('direct/<username>', views.directs, name="directs"),
    path('send/', views.send_directs, name="send-directs"),
    path('search/', views.user_search, name="search-users"),
    path('new/<username>', views.new_conversation, name="conversation"),
]
