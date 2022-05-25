from django.shortcuts import render
from posts.models import Post
from .models import Perfil
from django.contrib.auth.models import User
from .forms import UserUpdate, PerfilUpdate
from django.shortcuts import redirect
from notifications.models import Notifications
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

# RENDERS OTHER USER PROFILE

@login_required(login_url='login')
def renderizaPerfil(request, username):

        user_visitado = User.objects.get(username=username)
        posts = Post.objects.filter(usuario=user_visitado)
        my_profile = Perfil.objects.get(usuario=request.user)
        posts_list = []

        # USER POSTS

        for post in posts:
            posts_list.append(post)

        posts_list.sort(key=lambda x: x.data, reverse=True)

        # FOLLOW OR UNFOLLOW USER

        if request.method == 'POST':
            if user_visitado in my_profile.following.all():
                my_profile.following.remove(user_visitado)
                notification = Notifications.objects.get(notification_type=2, from_user=request.user, to_user=user_visitado)
                if notification:
                    notification.delete()
            else:
                my_profile.following.add(user_visitado)
                Notifications.objects.create(notification_type=2, from_user=request.user, to_user=user_visitado)

            redirect(user_visitado.perfil.get_absolute_url())

        # FOLLOWERS AND FOLOWING

        perfil_visitado = Perfil.objects.get(usuario=user_visitado)
        seguindo = perfil_visitado.following.all()
        seguidores = user_visitado.following.all()
        count_seguindo = len(seguindo)
        count_seguidores = len(seguidores)

        # =======================================================

        # WHO TO FOLLOW

        perfil_list = Perfil.objects.exclude(usuario=request.user)[:3]

        # NOTIFICATIONS

        user_notifications = Notifications.objects.filter(to_user=request.user).exclude(user_has_seen=True).count

        context = {
            'user': user_visitado,
            'posts': posts_list,
            'num_seguindo': count_seguindo,
            'num_seguidores': count_seguidores,
            'perfil_list': perfil_list,
            'user_notifications': user_notifications,
        }

        return render(request, 'profileapp/perfil.html', context=context)


# UPDATES USER PROFILE

@login_required(login_url='login')
def editarPerfil(request):

    if request.method == 'POST':
        u_form = UserUpdate(request.POST, instance=request.user)
        p_form = PerfilUpdate(request.POST, request.FILES, instance=request.user.perfil)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect(reverse_lazy('home'))

    u_form = UserUpdate(instance=request.user)
    p_form = PerfilUpdate(instance=request.user.perfil)

    # NOTIFICATIONS

    user_notifications = Notifications.objects.filter(to_user=request.user).exclude(user_has_seen=True).count

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'user_notifications': user_notifications,
    }
    return render(request, 'profileapp/editar-perfil.html', context=context)
