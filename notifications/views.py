# django built-in imports;
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
# current app imports;
from .models import Notifications


# render the notifications page;
@login_required(login_url='login')
def showNotifications(request):
    # queryset the notifications;
    user_notifications = Notifications.objects.filter(to_user=request.user).exclude(user_has_seen=True).order_by('-data')
    for notification in user_notifications:
        notification.user_has_seen = True
        notification.save()

    context = {
        'user_notifications': user_notifications,
    }

    return render(request, 'notifications/notifications.html', context=context)
