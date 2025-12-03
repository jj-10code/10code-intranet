from django.middleware.csrf import get_token
from inertia import share
from django.contrib import messages

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
            # Priorizar avatar subido, luego avatar_url de Google
            avatar_url = None
            if hasattr(request.user, 'avatar') and request.user.avatar:
                avatar_url = request.user.avatar.url
            elif hasattr(request.user, 'avatar_url') and request.user.avatar_url:
                avatar_url = request.user.avatar_url
                
            share(request, auth={
                'user': {
                    'id': request.user.id,
                    'name': request.user.get_full_name() or request.user.username,
                    'email': request.user.email,
                    'avatar': avatar_url,
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

class InertiaFlashMessagesMiddleware:
    """Comparte mensajes flash de Django con Inertia."""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        if request.user.is_authenticated:
            # Compartir mensajes flash
            storage = messages.get_messages(request)
            
            flash_messages = []
            for message in storage:
                flash_messages.append({
                    'type': message.level_tag,  # success, error, warning, info
                    'message': str(message),
                })
            
            share(request, 
                flash=flash_messages,
                errors=request.session.get('errors', {}),
            )
        
        return self.get_response(request)