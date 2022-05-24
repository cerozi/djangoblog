from django.urls import path
from .views import showNotifications

urlpatterns = [
    # NOTIFICATIONS
    path('notificacoes/', showNotifications, name='notificacoes')
]