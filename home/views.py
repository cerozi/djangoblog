# django built-in apps imports;
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.list import ListView

# other app imports;
from posts.forms import PostForm


# newsfeed/home view
@login_required(login_url='login')
def home(request):

    # form instance;
    form = PostForm()

    # followers and following queryset;
    following = len(request.user.perfil.following.all())
    followers = len(request.user.following.all())

    # returns a posts_list with all the posts from the users that the logged user is following;
    from profileapp.models import Perfil
    posts_list = Perfil.return_newsfeed_posts(request.user.perfil)

    # returns a queryset with all the profiles; this list is used to be displayed...
    # ...at the 'who to follow';
    perfil_list = Perfil.objects.exclude(usuario=request.user)[:3]

    context = {
        'seguidores': followers,
        'seguindo': following,
        'form': form,
        'posts_list': posts_list,
        'perfil_list': perfil_list,
    }

    return render(request, 'home/newsfeed.html', context=context)



# view for searching user;
@method_decorator(login_required(login_url='login'), name='get')
class userList(ListView):
    model = User
    template_name = 'home/search-user.html'

    # queryset of users based on the 'username' html input;
    def get_queryset(self):
        username_txt = self.request.GET.get('username')
        if username_txt:
            self.object_list = User.objects.filter(username__icontains=username_txt).exclude(username=self.request.user)
        else:
            self.object_list = User.objects.exclude(username=self.request.user).exclude(username='admin')
        return self.object_list
