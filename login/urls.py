from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import UsuarioCreate, login_view


urlpatterns = [

    # AUTENTICAÇÃO DE LOGIN

    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # CADASTRO DE NOVOS USUÁRIOS

    path('cadastro/', UsuarioCreate.as_view(), name='cadastro-usuário'),

]