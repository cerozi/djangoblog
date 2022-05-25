from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from .forms import UserRegistrationForm
from profileapp.models import Perfil
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from .decorators import deny_logged_user_access

# CREATE USER
@method_decorator(deny_logged_user_access, name='dispatch')
class UsuarioCreate(CreateView):
    template_name = 'cadastro/cadastro-usuario.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')
