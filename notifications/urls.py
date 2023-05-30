from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_notification, name='show-notification'),
    path('<id>/delete', views.delete_notification, name='delete-notification')
]