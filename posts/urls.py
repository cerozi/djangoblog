from django.urls import path
from .views import PostDelete, PostDetail, PostUpdate, PostCreate

urlpatterns = [
    path('excluir/post/<int:pk>', PostDelete, name='excluir-post'),
    path('editar/post/<int:pk>', PostUpdate, name='editar-post'),
    path('criar/post/', PostCreate, name='criar-post'),
    path('post/<int:pk>', PostDetail, name='post-detail')

]