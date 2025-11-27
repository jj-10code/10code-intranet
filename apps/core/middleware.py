from django.middleware.csrf import get_token
from inertia import share

class InertiaShareMiddleware:
    """
    Middleware que comparte datos globales con todas las respuestas de Inertia.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Compartir CSRF token
        share(request, csrf_token=get_token(request))
        
        # Compartir información del usuario autenticado
        if request.user.is_authenticated:
            share(request, auth={
                'user': {
                    'id': request.user.id,
                    'name': request.user.get_full_name() or request.user.username,
                    'email': request.user.email,
                    'avatar': None,  # TODO: implementar sistema de avatares
                },
                'permissions': []  # TODO: implementar sistema de permisos
            })
        else:
            share(request, auth={
                'user': None,
                'permissions': []
            })
        
        response = self.get_response(request)
        return response
