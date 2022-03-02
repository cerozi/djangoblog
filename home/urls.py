from django.urls import path
from .views import home, renderizaPerfil, editarPerfil, userList, showNotifications
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),

    # ACESSAR PERFIL

    path('perfil/<str:username>/', renderizaPerfil, name='perfil'),

    # EDIÇÃO DE PERFIL

    path('editar/', editarPerfil, name='editar-perfil'),

    # FILTRO DE PESQUISA DE USÚARIOS

    path('search-user/', userList.as_view(), name='search-user'),

    # NOTIFICAÇÕES

    path('notificacoes/', showNotifications, name='notificacoes')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)