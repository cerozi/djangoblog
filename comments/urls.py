from django.urls import path
from .views import CommentDelete, CommentUpdate

urlpatterns = [
    # deletes comment

    path('delete-comment/', CommentDelete, name='delete-comment'),

    # updates comment

    path('update-comment/', CommentUpdate, name='update-comment'),

]