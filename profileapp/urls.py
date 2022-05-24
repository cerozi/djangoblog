from django.urls import path 
from .views import renderizaPerfil, editarPerfil

urlpatterns = [
    # USER PROFILE

    path('perfil/<str:username>/', renderizaPerfil, name='perfil'),

    # UPDATES PROFILE

    path('editar/', editarPerfil, name='editar-perfil'),

]