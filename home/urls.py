from django.urls import path
from .views import home, userList
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),

    # FILTER FOR USER SEARCH

    path('search-user/', userList.as_view(), name='search-user'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)