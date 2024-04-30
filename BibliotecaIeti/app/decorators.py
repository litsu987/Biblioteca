from functools import wraps
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

def bibliotecari_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.rol == 'Bibliotecari':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('')  # Redirige a la página de inicio si el usuario no tiene el rol adecuado
    return wrapper

def alumne_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.rol == 'Alumne':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('')  # Redirige a la página de inicio si el usuario no tiene el rol adecuado
    return wrapper