from threading import local

_user = local()

def get_current_user():
    return getattr(_user, 'value', None)

class CurrentUserMiddleware:
    """Middleware para capturar el usuario actual en cada request."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _user.value = request.user
        response = self.get_response(request)
        _user.value = None
        return response
