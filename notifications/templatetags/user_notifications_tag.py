from django import template
from notifications.models import Notifications

register = template.Library()

@register.simple_tag
def return_notifications_count(user, *args, **kwargs):
    return Notifications.objects.filter(to_user=user, user_has_seen=False).count()
