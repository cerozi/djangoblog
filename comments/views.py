from django.shortcuts import render
from notifications.models import Notifications
from .models import Comments
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from profileapp.models import Perfil
from .forms import CommentForm

# Create your views here.
# DELETING COMMENTS

def CommentDelete(request):
    if request.method == 'POST':
        comment_pk = request.POST.get('comment_pk')
        comment_obj = get_object_or_404(Comments, usuario=request.user, pk=comment_pk)

        notification = Notifications.objects.get(notification_type=1, from_user=request.user, to_user=comment_obj.post.usuario, post=comment_obj.post, pk=comment_obj.pk)
        notification.delete()

        comment_obj.delete()

        post = comment_obj.post
        post.num_comments -= 1
        post.save()


        return redirect(post.get_absolute_url())
    else:
        return redirect(reverse_lazy('home'))

# UPDATING COMMENT

def CommentUpdate(request):

    # EDITING COMENNT

    comment_pk = request.GET.get('comment_pk')
    comment_obj = Comments.objects.get(pk=comment_pk, usuario=request.user)

    if comment_obj == None:
        return redirect(reverse_lazy('home'))

    if request.method == 'POST':
        comment_form = CommentForm(request.POST, instance=comment_obj)
        if comment_form.is_valid():
            comment_form.save()
            return redirect(comment_obj.post.get_absolute_url())

    comment_form = CommentForm(instance=comment_obj)

    # COMMENT'S LIST ON THE CURRENT POST

    post_comments = list(comment_obj.post.comments_set.all())
    post_comments.sort(key=lambda x: x.data, reverse=True)

    # POST DETAIL

    post_obj = comment_obj.post

    # WHO TO FOLLOW

    perfil_list = Perfil.objects.exclude(usuario=request.user)[:3]

    # FOLLOWERS E FOLLOWING

    following = len(request.user.perfil.following.all())
    followers = len(request.user.following.all())

    # NOTIFICATIONS

    count_notifications = Notifications.objects.filter(to_user=request.user).exclude(user_has_seen=True).count

    # CONTEXT

    context = {
        'post_obj': post_obj,
        'post_comments': post_comments,
        'comment_form': comment_form,
        'perfil_list': perfil_list,
        'followers': followers,
        'following': following,
        'comment_obj': comment_obj,
        'count_notifications': count_notifications,

    }

    return render(request, 'comments/editar-comment.html', context=context)