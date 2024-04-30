from django.http import Http404

def check_user_able_to_see_page(*rols):
    def decorator(function):
        def wrapper(request, *args, **kwargs):
            if request.user.rol in rols:
                return function(request, *args, **kwargs)
            raise Http404
        return wrapper
    return decorator
