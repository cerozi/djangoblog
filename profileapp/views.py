# django built-in apps imports;
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
# other apps imports;
from notifications.models import Notifications
from notifications.signals import follow_signal
from posts.models import Post
# current app imports;
from .forms import PerfilUpdate, UserUpdate
from .models import Perfil


# render profile;
@login_required(login_url='login')
def renderizaPerfil(request, username):

        # return a list with all the posts from the user;
        from posts.models import Post
        user_visitado = User.objects.get(username=username)
        posts_list = Post.return_user_posts(None, user=user_visitado)

        # FOLLOWERS AND FOLOWING

        perfil_visitado = Perfil.objects.get(usuario=user_visitado)
        seguindo = perfil_visitado.following.all()
        seguidores = user_visitado.following.all()
        count_seguindo = len(seguindo)
        count_seguidores = len(seguidores)

        # =======================================================

        # WHO TO FOLLOW

        perfil_list = Perfil.objects.exclude(usuario=request.user)[:3]

        context = {
            'user': user_visitado,
            'posts': posts_list,
            'num_seguindo': count_seguindo,
            'num_seguidores': count_seguidores,
            'perfil_list': perfil_list,
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
        notification = Notifications.objects.filter(notification_type=2, from_user=request.user, to_user=user)
        if notification.exists():
            notification[0].delete()
    else:
        logged_user.following.add(user) # if dont, follows;
        follow_signal.send(None, from_user=logged_user.usuario, to_user=user) # creates a notification;

    return redirect(reverse('perfil', args=[user.username]))
