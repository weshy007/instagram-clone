from django.shortcuts import render, redirect

from .models import Notification


# Create your views here.
def show_notification(request):
    user = request.user
    notifications = Notification.objects.filter(user=user).order_by('-date')

    context = {
        'notifications': notifications,
    }

    return render(request, 'notifications/notification.html', context)


def delete_notification(request, id):
    user = request.user
    Notification.objects.filter(id=id, user=user).delete()
    return redirect('show-notification')
