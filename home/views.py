from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from posts.models import Post, Likes, Notifications
from login.models import Perfil
from django.contrib.auth.models import User
from posts.forms import PostForm
from home.forms import UserUpdate, PerfilUpdate
from django.views.generic.list import ListView

# VIEW DO NEWSFEED/HOME

def home(request):

    if not request.user.is_authenticated:
        return redirect('/login/')

    else:

        # CRIAÇÃO DE POST

        form = PostForm()
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                txt = form.data['texto']
                new_post = Post.objects.create(usuario=request.user, texto = txt)
                Likes.objects.create(post=new_post)
                return redirect(reverse_lazy('home'))

        # BUSCA OS SEGUIDORES E SEGUINDO

        following = len(request.user.perfil.following.all())
        followers = len(request.user.following.all())

        # LISTA DE POSTS

        posts_list = []

        my_profile_following = request.user.perfil.following.all()

        for user in my_profile_following:
            user_posts = Post.objects.filter(usuario=user)
            for post in user_posts:
                posts_list.append(post)

        my_posts = Post.objects.filter(usuario=request.user)

        for post in my_posts:
            posts_list.append(post)

        posts_list.sort(key=lambda x: x.data, reverse=True)

        # PERFIS - WHO TO FOLLOW

        perfil_list = Perfil.objects.exclude(usuario=request.user)[:3]

        # NOTIFICAÇÕES

        user_notifications = Notifications.objects.filter(to_user=request.user).exclude(user_has_seen=True).count

        context = {
            'seguidores': followers,
            'seguindo': following,
            'form': form,
            'posts_list': posts_list,
            'perfil_list': perfil_list,
            'user_notifications': user_notifications,
        }

        return render(request, 'home/newsfeed.html', context=context)






# RENDERIZA O PERFIL VISITADO

def renderizaPerfil(request, username):

        user_visitado = User.objects.get(username=username)
        posts = Post.objects.filter(usuario=user_visitado)
        my_profile = Perfil.objects.get(usuario=request.user)
        posts_list = []

        for post in posts:
            posts_list.append(post)

        posts_list.sort(key=lambda x: x.data, reverse=True)

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

        # SEGUINDO E SEGUIDORES

        perfil_visitado = Perfil.objects.get(usuario=user_visitado)
        seguindo = perfil_visitado.following.all()
        seguidores = user_visitado.following.all()
        count_seguindo = len(seguindo)
        count_seguidores = len(seguidores)

        # =======================================================

        # PERFIS - WHO TO FOLLOW

        perfil_list = Perfil.objects.exclude(usuario=request.user)[:3]

        # NOTIFICAÇÕES

        user_notifications = Notifications.objects.filter(to_user=request.user).exclude(user_has_seen=True).count

        context = {
            'user': user_visitado,
            'posts': posts_list,
            'num_seguindo': count_seguindo,
            'num_seguidores': count_seguidores,
            'perfil_list': perfil_list,
            'user_notifications': user_notifications,
        }

        return render(request, 'home/perfil.html', context=context)


# EDITAR PERFIL DO USÚARIO

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

    # NOTIFICAÇÕES

    user_notifications = Notifications.objects.filter(to_user=request.user).exclude(user_has_seen=True).count

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'user_notifications': user_notifications,
    }
    return render(request, 'home/editar-perfil.html', context=context)

# FILTRO DE PESQUISA POR USÚARIO

class userList(ListView):
    model = User
    template_name = 'home/search-user.html'

    def get_queryset(self):
        
        username_txt = self.request.GET.get('username')

        if username_txt:
            self.object_list = User.objects.filter(username__icontains=username_txt).exclude(username=self.request.user)
        else:
            self.object_list = User.objects.exclude(username=self.request.user).exclude(username='admin')

        return self.object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['user_notifications'] = Notifications.objects.filter(to_user=self.request.user).exclude(user_has_seen=True).count

        return context

# VIEW DE NOTIFICAÇÕES DO USER

def showNotifications(request):

    user_notifications = Notifications.objects.filter(to_user=request.user).exclude(user_has_seen=True).order_by('-data')

    for notification in user_notifications:
        notification.user_has_seen = True
        notification.save()

    count_notifications = Notifications.objects.filter(to_user=request.user).exclude(user_has_seen=True).count

    context = {
        'user_notifications': user_notifications,
        'count_notifications': count_notifications,
    }

    return render(request, 'home/notifications.html', context=context)