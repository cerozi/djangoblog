# django built-in app imports;
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse

# other app imports;
from profileapp.models import Perfil
from posts.models import Post
from notifications.views import exclude_notification

# current app imports;
from .forms import CommentForm
from .models import Comments


# delete comment;
def CommentDelete(request):
    if request.method != 'POST':
        return redirect(reverse_lazy('home'))

    # gets the comment primary key from the html;
    comment_pk = request.POST.get('comment_pk')
    comment_obj = get_object_or_404(Comments, usuario=request.user, pk=comment_pk)

    exclude_notification(1, request.user, comment_obj.post.usuario, comment=comment_obj)

    comment_obj.delete()

    # updates the amount of comments associated to that current post;
    post = comment_obj.post
    post.num_comments -= 1
    post.save()

    return redirect(post.get_absolute_url())

# updates comment;
def CommentUpdate(request):

    # gets the comment primary key from the html;
    comment_pk = request.GET.get('comment_pk')
    comment_qs = Comments.objects.filter(pk=comment_pk, usuario=request.user)
    if not (comment_qs.exists()): # checks if the comment exists;
        return redirect(reverse_lazy('home'))

    # updates comment;
    comment_obj = comment_qs[0]
    if request.method == 'POST':
        comment_form = CommentForm(request.POST, instance=comment_obj)
        if comment_form.is_valid():
            comment_form.save()
            return redirect(comment_obj.post.get_absolute_url())

    comment_form = CommentForm(instance=comment_obj)

    # returns a list with all the comments associated to that post;
    from posts.models import Post
    post_comments = Post.return_post_comments(comment_obj.post)

    # who to follow queryset;
    perfil_list = Perfil.objects.exclude(usuario=request.user)[:3]

    # followers and following amount;
    following = len(request.user.perfil.following.all())
    followers = len(request.user.following.all())

    # context
    context = {
        'post_obj': comment_obj.post,
        'post_comments': post_comments,
        'comment_form': comment_form,
        'perfil_list': perfil_list,
        'followers': followers,
        'following': following,
        'comment_obj': comment_obj,

    }

    return render(request, 'comments/editar-comment.html', context=context)

# creates a comment;
def CommentCreate(request, pk):
    if request.method != 'POST':
        return redirect(reverse('home'))

    form = CommentForm(request.POST)
    post = Post.objects.get(pk=pk)
    if form.is_valid():
        form.instance.usuario = request.user # associates the comment to that logged user;
        form.instance.post = post # associates the comment to the post;
        form.save()

    return redirect(post.get_absolute_url())