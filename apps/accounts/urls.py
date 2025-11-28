"""
URLs del módulo de Autenticación y Usuarios.
"""

from django.urls import path

from apps.accounts import views

urlpatterns = [
    # Autenticación
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    # Dashboard
    path("dashboard/", views.dashboard_view, name="dashboard"),
    # Perfil
    path("profile/", views.profile_view, name="profile"),
    # Usuarios
    path("users/", views.users_index, name="users_index"),
]
