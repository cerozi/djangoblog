from django.db import models
from django.contrib.auth.models import User
from posts.models import Post

# Create your models here.
class Comments(models.Model):
    texto = models.TextField()
    data = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    curtidas = models.ManyToManyField(User, related_name='curtidas_comment')

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.texto