from django.urls import path
from .views import showNotifications

urlpatterns = [
    path('notificacoes/', showNotifications, name='notificacoes')
]