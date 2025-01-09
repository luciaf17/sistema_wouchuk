from threading import local
from django.shortcuts import redirect
from django.conf import settings

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
    
class LoginRequiredMiddleware:
    """
    Middleware para requerir login en todas las vistas.
    Excluye URLs configuradas en `LOGIN_EXEMPT_URLS`.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        login_exempt_urls = ['/login/', '/logout/']  # Agrega más URLs si es necesario
        if not request.user.is_authenticated and request.path not in login_exempt_urls:
            return redirect(settings.LOGIN_URL)
        return self.get_response(request)
