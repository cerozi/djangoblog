from django.urls import path
from .views import CommentDelete, CommentUpdate, CommentCreate

urlpatterns = [
    # deletes comment

    path('delete-comment/', CommentDelete, name='delete-comment'),

    # updates comment

    path('update-comment/', CommentUpdate, name='update-comment'),

    # updates comment

    path('create-comment/<int:pk>/', CommentCreate, name='comment-create'),

]