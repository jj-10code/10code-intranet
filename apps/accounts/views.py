"""
Vistas del módulo de Autenticación y Usuarios.

Vistas thin que solo preparan props para Inertia.js (frontend React).
La lógica de negocio está en services.py.
"""

from allauth.socialaccount.models import SocialAccount
from inertia import render

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods

from apps.accounts.services import AuthService


@require_http_methods(["GET"])
def login_view(request: HttpRequest) -> HttpResponse:
    """
    Vista de login.

    Renderiza página de login con botón de Google OAuth.
    Si el usuario ya está autenticado, redirige al dashboard.
    """
    # Si ya está autenticado, redirigir al dashboard
    if request.user.is_authenticated:
        return redirect("dashboard")

    return render(
        request,
        "auth/Login",
        props={
            "google_login_url": "/accounts/google/login/",
            "title": "Iniciar Sesión - 10Code Intranet",
        },
    )


@login_required
@require_http_methods(["POST"])
def logout_view(request: HttpRequest) -> HttpResponse:
    """
    Vista de logout.

    Cierra sesión del usuario y registra en AuditLog.
    """
    user = request.user

    # Procesar logout con Service Layer
    AuthService.logout_user(request=request, user=user)

    # Redirigir al login
    return redirect("login")


@login_required
@require_http_methods(["GET"])
def dashboard_view(request: HttpRequest) -> HttpResponse:
    """
    Vista del dashboard principal.

    Muestra información básica del usuario y links a módulos.
    """
    user = request.user

    # Obtener perfil de Google si existe
    try:
        google_profile = SocialAccount.objects.get(user=user, provider="google")
        google_data = google_profile.extra_data
    except SocialAccount.DoesNotExist:
        google_data = {}

    # Obtener roles del usuario
    user_roles = list(user.user_roles.select_related("role").values_list("role__name", flat=True))

    return render(
        request,
        "Dashboard",
        props={
            "user": {
                "id": user.id,
                "email": user.email,
                "full_name": user.get_full_name(),
                "first_name": user.first_name,
                "last_name": user.last_name,
                "avatar_url": user.avatar_url or google_data.get("picture", ""),
                "is_staff": user.is_staff,
                "is_superuser": user.is_superuser,
                "roles": user_roles,
            },
            "title": "Dashboard - 10Code Intranet",
        },
    )


@login_required
@require_http_methods(["GET"])
def profile_view(request: HttpRequest) -> HttpResponse:
    """
    Vista del perfil de usuario.

    Muestra información completa del perfil.
    """
    user = request.user

    # Obtener Google Profile si existe
    try:
        google_profile = user.google_profile
        google_data = google_profile.raw_data
    except Exception:
        google_data = {}

    # Obtener roles con detalles
    user_roles = [
        {
            "code": ur.role.code,
            "name": ur.role.name,
            "assigned_at": ur.assigned_at.isoformat(),
        }
        for ur in user.user_roles.select_related("role")
    ]

    return render(
        request,
        "profile/Show",
        props={
            "user": {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "full_name": user.get_full_name(),
                "avatar_url": user.avatar_url,
                "date_joined": user.date_joined.isoformat(),
                "last_login": user.last_login.isoformat() if user.last_login else None,
                "is_staff": user.is_staff,
                "roles": user_roles,
            },
            "google_data": google_data,
            "title": "Mi Perfil - 10Code Intranet",
        },
    )


@login_required
@require_http_methods(["GET"])
def users_index(request: HttpRequest) -> HttpResponse:
    """
    Vista de listado de usuarios.
    """
    from django.contrib.auth import get_user_model
    
    User = get_user_model()
    users = User.objects.all().values('id', 'first_name', 'last_name', 'email')
    
    # Formatear datos para el frontend
    users_list = [
        {
            'id': user['id'],
            'name': f"{user['first_name']} {user['last_name']}".strip() or 'Sin nombre',
            'email': user['email'],
        }
        for user in users
    ]
    
    return render(request, 'Users/Index', props={
        'users': users_list
    })
