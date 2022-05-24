from django.shortcuts import render
from notifications.models import Notifications
from posts.models import Post
from .models import Likes
from django.shortcuts import redirect
from django.urls import reverse_lazy
from comments.models import Comments

# Create your views here.
# LIKING THE POST

def PostLike(request):

    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = Post.objects.get(pk=post_id)
        
        if request.user in post.curtidas.all():
            post.curtidas.remove(request.user)
            notification = Notifications.objects.get(notification_type=0, from_user=request.user, to_user=post.usuario, post=post)
            notification.delete()
        else:
            post.curtidas.add(request.user)
            Notifications.objects.create(notification_type=0, from_user=request.user, to_user=post.usuario, post=post)

        likes_obj = Likes.objects.get(post=post)
        likes_obj.quantidade = len(post.curtidas.all())
        likes_obj.save()

    return redirect(reverse_lazy('home'))

# LIKING A COMMENT

def CommentLike(request):
    if request.method == 'POST':
        comment_pk = request.POST.get('comment_pk')
        comment_obj = Comments.objects.get(pk=comment_pk)

        if request.user in comment_obj.curtidas.all():
            comment_obj.curtidas.remove(request.user)
            notification = Notifications.objects.get(notification_type=0, from_user=request.user, to_user=comment_obj.usuario, comment=comment_obj)
            notification.delete()
        else:
            comment_obj.curtidas.add(request.user)
            Notifications.objects.create(notification_type=0, from_user=request.user, to_user=comment_obj.usuario, comment=comment_obj)

        likes_obj = Likes.objects.get(comment=comment_obj)
        likes_obj.quantidade = len(comment_obj.curtidas.all())
        likes_obj.save()

        post = comment_obj.post

        return redirect(post.get_absolute_url())
    else:
        return redirect(reverse_lazy('home'))