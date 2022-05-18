from django.urls import path
from .views import home, renderizaPerfil, editarPerfil, userList, showNotifications
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),

    # USER PROFILE

    path('perfil/<str:username>/', renderizaPerfil, name='perfil'),

    # UPDATES PROFILE

    path('editar/', editarPerfil, name='editar-perfil'),

    # FILTER FOR USER SEARCH

    path('search-user/', userList.as_view(), name='search-user'),

    # NOTIFICATIONS

    path('notificacoes/', showNotifications, name='notificacoes')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)