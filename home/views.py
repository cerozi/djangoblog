from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from posts.models import Post
from likes.models import Likes
from notifications.models import Notifications
from profileapp.models import Perfil
from django.contrib.auth.models import User
from posts.forms import PostForm
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# NEWSFEED/HOME

@login_required(login_url='login')
def home(request):
    # POST CREATION

    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            txt = form.data['texto']
            new_post = Post.objects.create(usuario=request.user, texto = txt)
            Likes.objects.create(post=new_post)
            return redirect(reverse_lazy('home'))

    # FOLLOWERS AND FOLOWING

    following = len(request.user.perfil.following.all())
    followers = len(request.user.following.all())

    # POSTS LIST
    from profileapp.models import Perfil
    posts_list = Perfil.return_newsfeed_posts(request.user.perfil)
    # WHO TO FOLLOW PROFILES

    perfil_list = Perfil.objects.exclude(usuario=request.user)[:3]

    # NOTIFICATIONS

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



# FILTER FOR USER 

@method_decorator(login_required(login_url='login'), name='get')
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