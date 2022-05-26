from django.urls import path
from .views import PostLike, CommentLike

urlpatterns = [
    path('like-post/', PostLike, name='like-post'),
    path('like-comment/', CommentLike, name='like-comment'),

]