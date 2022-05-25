from xml.etree.ElementTree import Comment
from django.db import models
from posts.models import Post
from comments.models import Comments
from django.db.models.signals import post_save

# Create your models here.
class Likes(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, null = True)
    comment = models.OneToOneField(Comments, on_delete=models.CASCADE, null=True)
    quantidade = models.IntegerField(default=0)

# django signals for creating a model Like everytime...
# ... a post object is created;
def create_like_for_post(sender, instance, created, **kwargs):
    if created:
        Likes.objects.create(post=instance)

post_save.connect(create_like_for_post, sender=Post)


# django signals for creating a model Like everytime...
# ... a comment object is created;
def create_like_for_comment(sender, instance, created, **kwargs):
    if created:
        Likes.objects.create(comment=instance)

post_save.connect(create_like_for_comment, sender=Comments)
