# django built-in imports
from django.shortcuts import redirect
from django.urls import reverse_lazy
# other apps imports
from notifications.models import Notifications
from notifications.signals import like_signal
from posts.models import Post
from comments.models import Comments
# current app imports
from .models import Likes


# liking a post;
def PostLike(request):

    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = Post.objects.get(pk=post_id)
        
        # checks if the user already liked the post;
        if request.user in post.curtidas.all(): # if so, delete the notification and takes the user from 'many to many' relation;
            post.curtidas.remove(request.user)
            notification = Notifications.objects.filter(notification_type=0, 
                                        from_user=request.user, 
                                        to_user=post.usuario, post=post)
            if notification.exists():
                notification[0].delete()
        else: 
            post.curtidas.add(request.user) # adds user to the 'many to many' relation on the post object;
            like_signal.send(sender=None, instance=post, user=request.user) # sends a signal to create a notification;
            

        # updates the like object;
        likes_obj = Likes.objects.get(post=post)
        likes_obj.quantidade = len(post.curtidas.all())
        likes_obj.save()

    return redirect(reverse_lazy('home'))


# liking a comment
def CommentLike(request):
    if request.method == 'POST':
        comment_pk = request.POST.get('comment_pk')
        comment_obj = Comments.objects.get(pk=comment_pk)

        # checks if the user already liked the comment;
        if request.user in comment_obj.curtidas.all(): # if so, delete the notification and takes the user from 'many to many' relation;
            comment_obj.curtidas.remove(request.user)
            notification = Notifications.objects.filter(notification_type=0, from_user=request.user, 
                                                        to_user=comment_obj.usuario, comment=comment_obj)
            if notification.exists():
                notification[0].delete()
        else:
            comment_obj.curtidas.add(request.user) # adds user to the 'many to many' relation on the post object;
            like_signal.send(sender=None, instance=comment_obj, user=request.user) # sends a signal to create a notification;

        # updates the like object;
        likes_obj = Likes.objects.get(comment=comment_obj)
        likes_obj.quantidade = len(comment_obj.curtidas.all())
        likes_obj.save()

        post = comment_obj.post
        return redirect(post.get_absolute_url())
    
    return redirect(reverse_lazy('home'))
