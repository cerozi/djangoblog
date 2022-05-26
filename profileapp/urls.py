from django.urls import path 
from .views import renderizaPerfil, editarPerfil, followuser

urlpatterns = [
    path('perfil/<str:username>/', renderizaPerfil, name='perfil'),
    path('follows/<str:username>/', followuser, name='follow-user'),
    path('editar/', editarPerfil, name='editar-perfil'),

]