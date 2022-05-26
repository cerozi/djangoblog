# django built-in app imports;
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
# other apps imports;
from profileapp.models import Perfil
from comments.forms import CommentForm
# current app imports;
from .forms import PostForm
from .models import Post


# creates a post;
def PostCreate(request):
    if request.method != 'POST':
        return redirect(reverse('home'))

    form = PostForm(request.POST)
    if form.is_valid():
        form.instance.usuario = request.user
        form.save()
        return redirect(reverse('home'))

# updating a post;
def PostUpdate(request, pk):
    # checks if the post exists;
    post_qs = Post.objects.filter(pk=pk, usuario=request.user)
    if not post_qs.exists():
        return redirect(reverse_lazy('home'))
    post_obj = post_qs[0]

    # updates the post
    post = PostForm(instance=post_obj)
    if request.method == 'POST':
        post = PostForm(request.POST, instance=post_obj)
        if post.is_valid():
            post.save()
            return redirect(reverse_lazy('home'))

    # returns all the comments from that post
    from .models import Post
    post_comments = Post.return_post_comments(post_obj)

    # profile queryset
    perfil_list = Perfil.objects.exclude(usuario=request.user)[:3]

    context = {
        'post': post,
        'perfil_list': perfil_list,
        'post_comments': post_comments,
    }

    return render(request, 'posts/editar-post.html', context=context)

# deletes a post;
def PostDelete(request, pk):
    if request.method == 'POST':
        obj = Post.objects.get(pk=pk, usuario=request.user)
        obj.delete()

    return redirect(reverse_lazy('home'))

# post detail;
@login_required(login_url='login')
def PostDetail(request, pk):

    # form for comment;
    comment_form = CommentForm()

    # returns all the comments from that post
    from .models import Post
    post = Post.objects.get(pk=pk)
    post_comments = Post.return_post_comments(post)

    # WHO TO FOLLOW

    perfil_list = Perfil.objects.exclude(usuario=request.user)[:3]

    # FOLLOWERS AND FOLLOWING

    my_profile = Perfil.objects.get(usuario=request.user)
    following = len(my_profile.following.all())
    followers = len(my_profile.usuario.following.all())

    context = {
        'post': post,
        'perfil_list': perfil_list,
        'comment_form': comment_form,
        'post_comments': post_comments,
        'following': following,
        'followers': followers,
    }

    return render(request, 'posts/post-detail.html', context=context)
