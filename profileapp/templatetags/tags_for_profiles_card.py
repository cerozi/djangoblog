from django import template
from profileapp.models import Perfil

register = template.Library()

@register.inclusion_tag('base_templates/profiles-card.html', takes_context=True)
def profiles_card(context):
    request_user = context['request'].user
    perfil_list = Perfil.objects.all().exclude(usuario=request_user).order_by('-created')[:3]
    return {'perfil_list': perfil_list}