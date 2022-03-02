from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from .forms import UserRegistrationForm
from .models import Perfil
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class UsuarioCreate(CreateView):
    template_name = 'cadastro/cadastro-usuario.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):

        url = super().form_valid(form)

        Perfil.objects.create(usuario=self.object, nome=self.object.first_name)

        return url


class UsuarioUpdate(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    model = Perfil
    fields = ['nome', 'telefone', 'sexo', 'email']
    template_name = 'cadastro/cadastro-usuario.html'
    success_url = reverse_lazy('lista-posts')

    def get_object(self, queryset=None):
        
        self.object = get_object_or_404(Perfil, usuario=self.request.user)

        return self.object

