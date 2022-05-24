from django.db import models
from django.contrib.auth.models import User
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