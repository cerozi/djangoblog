# django built-in imports;
from django.contrib.auth.models import User
from django.db import models

# other apps imports;
from posts.models import Post
from comments.models import Comments


class Notifications(models.Model):
    # 0 = Like, 1 = Comment e 2 = Follow
    notification_type = models.IntegerField()
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(Comments, on_delete=models.CASCADE, null=True, blank=True)
    user_has_seen = models.BooleanField(default=False)
    data = models.DateTimeField(auto_now_add=True)
