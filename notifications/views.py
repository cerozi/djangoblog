from django.shortcuts import render
from .models import Notifications

# USER NOTIFICATIONS

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