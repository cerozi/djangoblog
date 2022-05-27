# django built-in apps imports;
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
# other apps imports;
from notifications.models import Notifications
from notifications.signals import follow_signal
from notifications.views import exclude_notification
from posts.models import Post
# current app imports;
from .forms import PerfilUpdate, UserUpdate
from .models import Perfil


# render profile;
@login_required(login_url='login')
def renderizaPerfil(request, username):

    # return a list with all the posts from the user;
    from posts.models import Post
    user = User.objects.get(username=username)
    posts_list = Post.return_user_posts(None, user=user)

    context = {
        'user': user,
        'posts': posts_list,
    }

    return render(request, 'profileapp/perfil.html', context=context)


# updates profile;
@login_required(login_url='login')
def editarPerfil(request):
    # updates profile and user info;
    if request.method == 'POST':
        u_form = UserUpdate(request.POST, instance=request.user)
        p_form = PerfilUpdate(request.POST, request.FILES, instance=request.user.perfil)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect(reverse_lazy('home'))
    # user and profile instance;
    u_form = UserUpdate(instance=request.user)
    p_form = PerfilUpdate(instance=request.user.perfil)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'profileapp/editar-perfil.html', context=context)


# follow/unfollows user;
def followuser(request, username):
    if request.method != 'POST':
        return redirect(reverse('home'))

    user = User.objects.get(username=username)
    logged_user = Perfil.objects.get(usuario=request.user)

    if user in logged_user.following.all(): # checks if the request user profile is associated to the user; 
        logged_user.following.remove(user) # if so, unfollows;
        exclude_notification(2, request.user, user)
    else:
        logged_user.following.add(user) # if dont, follows;
        follow_signal.send(None, from_user=logged_user.usuario, to_user=user) # creates a notification;

    return redirect(reverse('perfil', args=[user.username]))
