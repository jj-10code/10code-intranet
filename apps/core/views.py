from inertia import render
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse


@login_required
def dashboard_view(request):
    """
    Vista principal del dashboard.
    Renderiza la página Dashboard de React con datos del usuario.
    """
    return render(request, 'Dashboard', props={
        'user': {
            'name': request.user.get_full_name() or request.user.username,
            'email': request.user.email,
        }
    })

@login_required
def help_view(request):
    """
    Vista de ayuda.
    Renderiza la página Help de React.
    """
    return render(request, 'Help', props={
        'user': {
            'name': request.user.get_full_name() or request.user.username,
            'email': request.user.email,
            'avatar': request.user.avatar.url if hasattr(request.user, 'avatar') and request.user.avatar else None,
        }
    })

def handler403(request: HttpRequest, exception=None) -> HttpResponse:
    """
    Custom 403 error handler.
    Renders the Inertia 'Error' page with status 403.
    """
    from django.http import HttpResponse
    response = render(request, 'Error', props={'status': 403})
    response.status_code = 403
    return response
