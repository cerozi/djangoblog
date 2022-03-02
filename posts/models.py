from django.db import models
from login.models import User
from django.urls import reverse

# Create your models here.

class Post(models.Model):
    texto = models.TextField()
    data = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    curtidas = models.ManyToManyField(User, related_name='curtidas')
    num_comments = models.IntegerField(default=0)

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):

        return self.texto

    def get_absolute_url(self):
        return reverse('post-detail', args=[self.pk, ])

class Comments(models.Model):
    texto = models.TextField()
    data = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    curtidas = models.ManyToManyField(User, related_name='curtidas_comment')

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.texto

class Likes(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, null = True)
    comment = models.OneToOneField(Comments, on_delete=models.CASCADE, null=True)
    quantidade = models.IntegerField(default=0)


class Notifications(models.Model):
    # 0 = Like, 1 = Comment e 2 = Follow
    notification_type = models.IntegerField()
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(Comments, on_delete=models.CASCADE, null=True, blank=True)
    user_has_seen = models.BooleanField(default=False)
    data = models.DateTimeField(auto_now_add=True)
