from django.urls import path
from .views import CommentDelete, CommentUpdate, CommentCreate

urlpatterns = [
    path('delete-comment/', CommentDelete, name='delete-comment'),
    path('update-comment/', CommentUpdate, name='update-comment'),
    path('create-comment/<int:pk>/', CommentCreate, name='comment-create'),

]