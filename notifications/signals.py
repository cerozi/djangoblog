# django built-in imports
import django.dispatch
from django.db.models.signals import post_save, post_delete

# other apps imports;
from comments.models import Comments

# current app imports;
from .models import Notifications


# django signals receiver; creates a notification everytime a comment object is created.
def create_notification_for_comment(sender, instance, created, **kwargs):
    if created:
        Notifications.objects.create(
            notification_type = 1,
            to_user = instance.post.usuario,
            from_user = instance.usuario,
            comment = instance
        )

post_save.connect(create_notification_for_comment, sender=Comments)


# django signals receiver; creates a notification everytime a user like a post or a comment;
def create_like_notification(sender, instance, user, **kwargs):
    if type(instance).__name__ == 'Post': # if the user likes a post, then it creates a notification associated to that post;
        Notifications.objects.create(
            notification_type = 0,
            to_user = instance.usuario,
            from_user = user,
            post = instance
        )
    if type(instance).__name__ == 'Comments': # if the user likes a comment, then it creates a notification associated to that comment;
        Notifications.objects.create(
            notification_type = 0,
            to_user = instance.usuario,
            from_user = user,
            comment = instance
        )

like_signal = django.dispatch.Signal() # creating custom signal;
like_signal.connect(create_like_notification, sender=None)

# django signals receiver; creates a notification everytime a profile follows a user;
def create_follow_notification(sender, from_user, to_user, **kwargs):
    Notifications.objects.create(
        notification_type = 2,
        from_user = from_user,
        to_user = to_user
    )

follow_signal = django.dispatch.Signal()
follow_signal.connect(create_follow_notification, sender=None)