from django.urls import path
from .views import PostDelete, PostLike, PostDetail, CommentLike, CommentDelete, PostUpdate, CommentUpdate

urlpatterns = [

    # EXCLUIR POSTS 

    path('excluir/post/<int:pk>', PostDelete, name='excluir-post'),

    # EDITAR POSTS

    path('editar/post/<int:pk>', PostUpdate, name='editar-post'),

    # SUBMISSÃO DE LIKE NO POST

    path('like-post/', PostLike, name='like-post'),

    # DETAIL DO POST

    path('post/<int:pk>', PostDetail, name='post-detail'),

    # LIKE NO COMMENT

    path('like-comment/', CommentLike, name='like-comment'),

    # DELETAR COMMENT

    path('delete-comment/', CommentDelete, name='delete-comment'),

    # UPDATE COMMENT

    path('update-comment/', CommentUpdate, name='update-comment'),

]