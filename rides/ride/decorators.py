from django.core.exceptions import PermissionDenied
from functools import wraps

def admin_only(function):
    @wraps(function)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.groups.filter(name='Admin').exists():
            raise PermissionDenied("You do not have permission to access this resource.")
        return function(request, *args, **kwargs)
    return _wrapped_view
