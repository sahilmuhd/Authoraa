# utils.py
from django.http import HttpResponseForbidden

def role_required(role_name):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.role.name != role_name:
                return HttpResponseForbidden("You do not have access to this page.")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
