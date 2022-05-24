from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from .forms import UserRegistrationForm
from profileapp.models import Perfil
from django.contrib.auth.mixins import LoginRequiredMixin

# CREATE USER
class UsuarioCreate(CreateView):
    template_name = 'cadastro/cadastro-usuario.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):

        url = super().form_valid(form)

        Perfil.objects.create(usuario=self.object, nome=self.object.first_name)

        return url
