from django.urls import path
from .views import PostDelete, PostDetail, PostUpdate

urlpatterns = [

    # deleting posts

    path('excluir/post/<int:pk>', PostDelete, name='excluir-post'),

    # updating posts

    path('editar/post/<int:pk>', PostUpdate, name='editar-post'),

    # post detail

    path('post/<int:pk>', PostDetail, name='post-detail')

]