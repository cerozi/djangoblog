from django.forms import ModelForm
from django.contrib.auth.models import User
from profileapp.models import Perfil

class UserUpdate(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'username']

class PerfilUpdate(ModelForm):
    class Meta:
        model = Perfil
        fields = ['bio', 'foto']