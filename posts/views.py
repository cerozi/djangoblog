from django.shortcuts import get_object_or_404, redirect, render
from .models import Post, Likes, Comments, Notifications
from django.urls import reverse_lazy
from login.models import Perfil
from .forms import PostForm, CommentForm


def PostUpdate(request, pk):
    post_obj = Post.objects.get(pk=pk, usuario=request.user)

    if post_obj == None:
        return redirect(reverse_lazy('home'))

    post = PostForm(instance=post_obj)

    # EDITA A POSTAGEM

    if request.method == 'POST':
        post = PostForm(request.POST, instance=post_obj)
        if post.is_valid():
            post.save()
            return redirect(reverse_lazy('home'))

    # COMENTÁRIOS DO POST

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


def PostDelete(request, pk):
    if request.method == 'POST':
        obj = Post.objects.get(pk=pk, usuario=request.user)
        obj.delete()

    return redirect(reverse_lazy('home'))


def PostDetail(request, pk):

    # SUBMISSÃO DE COMENTÁRIO

    post = Post.objects.get(pk=pk)
    comment_form = CommentForm()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            txt = comment_form.data['texto']
            comment = Comments.objects.create(texto=txt, usuario=request.user, post=post)
            post.num_comments += 1
            post.save()

            Likes.objects.create(comment=comment)
            Notifications.objects.create(notification_type=1, from_user=request.user, to_user=post.usuario, post=post, pk=comment.pk)

            return redirect(post.get_absolute_url())

    # LISTA DE COMMENTS

    post_comments = list(post.comments_set.all())

    post_comments.sort(key=lambda x: x.data, reverse=True)

    # WHO TO FOLLOW

    perfil_list = Perfil.objects.exclude(usuario=request.user)[:3]

    # SEGUIDORES E SEGUINDO

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


# SUBMISSÃO DE LIKE NO POST

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

# ==================== COMENTÁRIOS ===============

# SUBMISSÃO DE LIKE NO COMENTÁRIO

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

# EXCLUSÃO DE COMENTÁRIOS

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

# UPDATE DE COMENTÁRIO

def CommentUpdate(request):

    # SUBMISSÃO DA EDIÇÃO DO COMMENT

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

    # LISTA DE COMENTÁRIOS DO POST

    post_comments = list(comment_obj.post.comments_set.all())
    post_comments.sort(key=lambda x: x.data, reverse=True)

    # DETAIL DO POST

    post_obj = comment_obj.post

    # WHO TO FOLLOW

    perfil_list = Perfil.objects.exclude(usuario=request.user)[:3]

    # FOLLOWERS E FOLLOWING

    following = len(request.user.perfil.following.all())
    followers = len(request.user.following.all())

    # NOTIFICATIONS

    count_notifications = Notifications.objects.filter(to_user=request.user).exclude(user_has_seen=True).count

    # CONTEXTO

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

    return render(request, 'posts/editar-comment.html', context=context)