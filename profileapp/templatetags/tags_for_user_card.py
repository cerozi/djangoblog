from django import template
from profileapp.models import Perfil

register = template.Library()

@register.inclusion_tag('base_templates/user-card.html', takes_context=True)
def user_card(context, user):
    request_user = context['request'].user
    profile = Perfil.objects.get(usuario=user)
    following = profile.following.all().count()
    followers = user.following.all().count()
    return {'user': user,
            'request_user': request_user,
            'first_name': user.first_name,
            'pic_url': profile.foto.url,
            'username': user.username,
            'bio': profile.bio,
            'following': following,
            'followers': followers
            }