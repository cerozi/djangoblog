from django.urls import path
from .views import PostDelete, PostLike, PostDetail, CommentLike, CommentDelete, PostUpdate, CommentUpdate

urlpatterns = [

    # deleting posts

    path('excluir/post/<int:pk>', PostDelete, name='excluir-post'),

    # updating posts

    path('editar/post/<int:pk>', PostUpdate, name='editar-post'),

    # liking a post

    path('like-post/', PostLike, name='like-post'),

    # post detail

    path('post/<int:pk>', PostDetail, name='post-detail'),

    # liking comments

    path('like-comment/', CommentLike, name='like-comment'),

    # deletes comment

    path('delete-comment/', CommentDelete, name='delete-comment'),

    # updates comment

    path('update-comment/', CommentUpdate, name='update-comment'),

]