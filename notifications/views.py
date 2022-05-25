from django.shortcuts import render
from .models import Notifications
from django.contrib.auth.decorators import login_required

# USER NOTIFICATIONS

@login_required(login_url='login')
def showNotifications(request):

    user_notifications = Notifications.objects.filter(to_user=request.user).exclude(user_has_seen=True).order_by('-data')

    for notification in user_notifications:
        notification.user_has_seen = True
        notification.save()

    count_notifications = Notifications.objects.filter(to_user=request.user).exclude(user_has_seen=True).count

    context = {
        'user_notifications': user_notifications,
        'count_notifications': count_notifications,
    }

    return render(request, 'notifications/notifications.html', context=context)