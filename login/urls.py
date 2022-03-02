from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import UsuarioCreate, UsuarioUpdate


urlpatterns = [

    # AUTENTICAÇÃO DE LOGIN

    path('login/', LoginView.as_view(
        template_name = 'login/login.html'
    ), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # CADASTRO DE NOVOS USUÁRIOS

    path('cadastro/', UsuarioCreate.as_view(), name='cadastro-usuário'),

]