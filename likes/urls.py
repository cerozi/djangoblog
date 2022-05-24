from django.urls import path
from .views import PostLike, CommentLike

urlpatterns = [
    # liking a post

    path('like-post/', PostLike, name='like-post'),

    # liking comments

    path('like-comment/', CommentLike, name='like-comment'),

]