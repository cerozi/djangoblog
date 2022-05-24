from django.db import models
from posts.models import Post
from comments.models import Comments

# Create your models here.
class Likes(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, null = True)
    comment = models.OneToOneField(Comments, on_delete=models.CASCADE, null=True)
    quantidade = models.IntegerField(default=0)