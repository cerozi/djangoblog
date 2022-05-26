# django built-in apps import;
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView
# current app imports;
from .decorators import deny_logged_user_access
from .forms import UserRegistrationForm


# class based view to create a new user;
@method_decorator(deny_logged_user_access, name='dispatch')
class UsuarioCreate(CreateView):
    template_name = 'cadastro/cadastro-usuario.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')

# login view;
@deny_logged_user_access
def login_view(request):
    if request.method != 'POST':
        form = AuthenticationForm()
        return render(request, 'login/login.html', {'form': form})
    
    form = AuthenticationForm(data=request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user = authenticate(request, username=username, password=password) # checks if the user exists;
        if user:
            login(request, user) # log user;
            return redirect(reverse('home'))

    return render(request, 'login/login.html', {'form': form})
