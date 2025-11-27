from inertia import render
from django.contrib.auth.decorators import login_required


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
