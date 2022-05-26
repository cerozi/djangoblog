# django built-in imports;
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
# current app imports;
from .models import Notifications


# render the notifications page;
@login_required(login_url='login')
def showNotifications(request):
    # queryset the notifications;
    user_notifications = Notifications.objects.filter(to_user=request.user).order_by('-data')
    for notification in user_notifications:
        notification.delete()

    context = {
        'user_notifications': user_notifications,
    }

    return render(request, 'notifications/notifications.html', context=context)


# deletes notification that was created from a like, comment or follow that the user unmade;
def exclude_notification(notif_type, from_user, to_user, post=None, comment=None):
    notif = Notifications.objects.filter(notification_type=notif_type, 
                                        from_user=from_user, to_user=to_user, 
                                        post=post, comment=comment)
    if notif.exists() and (not notif[0].user_has_seen):
        notif[0].delete()
