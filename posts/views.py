from django.shortcuts import get_object_or_404, redirect, render
from .models import Post
from likes.models import Likes
from comments.models import Comments
from notifications.models import Notifications
from django.urls import reverse_lazy
from profileapp.models import Perfil
from .forms import PostForm
from comments.forms import CommentForm
from django.contrib.auth.decorators import login_required


# UPDATES POST

def PostUpdate(request, pk):
    post_obj = Post.objects.get(pk=pk, usuario=request.user)

    if post_obj == None:
        return redirect(reverse_lazy('home'))

    post = PostForm(instance=post_obj)

    # UPDATES POST

    if request.method == 'POST':
        post = PostForm(request.POST, instance=post_obj)
        if post.is_valid():
            post.save()
            return redirect(reverse_lazy('home'))

    # POST'S COMMENTS

    post_comments = list(post_obj.comments_set.all())

    post_comments.sort(key=lambda x: x.data)

    # WHO TO FOLLOW

    perfil_list = Perfil.objects.exclude(usuario=request.user)[:3]

    # NOTIFICATIONS

    count_notifications = Notifications.objects.filter(to_user=request.user).exclude(user_has_seen=True).count

    # CONTEXT

    context = {
        'post': post,
        'perfil_list': perfil_list,
        'post_comments': post_comments,
        'count_notifications': count_notifications,
    }

    return render(request, 'posts/editar-post.html', context=context)

# POST DELETE

def PostDelete(request, pk):
    if request.method == 'POST':
        obj = Post.objects.get(pk=pk, usuario=request.user)
        obj.delete()

    return redirect(reverse_lazy('home'))

# GETS POST DETAIL

@login_required(login_url='login')
def PostDetail(request, pk):

    # COMMENTING ON THE CURRENT POST

    post = Post.objects.get(pk=pk)
    comment_form = CommentForm()

    # COMMENT'S LIST

    post_comments = list(post.comments_set.all())

    post_comments.sort(key=lambda x: x.data, reverse=True)

    # WHO TO FOLLOW

    perfil_list = Perfil.objects.exclude(usuario=request.user)[:3]

    # FOLLOWERS AND FOLLOWING

    my_profile = Perfil.objects.get(usuario=request.user)
    following = len(my_profile.following.all())
    followers = len(my_profile.usuario.following.all())

    # NOTIFICATIONS

    count_notifications = Notifications.objects.filter(to_user=request.user).exclude(user_has_seen=True).count

    context = {
        'post': post,
        'perfil_list': perfil_list,
        'comment_form': comment_form,
        'post_comments': post_comments,
        'following': following,
        'followers': followers,
        'count_notifications': count_notifications,
    }

    return render(request, 'posts/post-detail.html', context=context)