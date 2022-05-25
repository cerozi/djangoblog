from django.shortcuts import redirect
from django.urls import reverse

def deny_logged_user_access(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('home'))
        return view_func(request, *args, **kwargs)

    return wrapper