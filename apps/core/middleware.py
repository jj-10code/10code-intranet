from inertia import share
from django.contrib import messages

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
