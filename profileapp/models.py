from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Perfil(models.Model):

    SEXO_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Feminino'),
    )

    nome = models.CharField(max_length=255, null=True)
    telefone = models.CharField(max_length=12, null=True)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, null=True)
    email = models.EmailField(null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    following = models.ManyToManyField(User, related_name='following', blank=True)
    bio = models.CharField(max_length=100, default='Hello, World')
    foto = models.ImageField(default='default.png')

    usuario = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse('perfil', kwargs={'username': self.nome})
