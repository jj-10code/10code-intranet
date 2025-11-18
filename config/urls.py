"""
Configuración de URLs principal para 10Code Intranet.
"""

from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    # Admin de Django
    path("admin/", admin.site.urls),
    # Autenticación con django-allauth
    path("accounts/", include("allauth.urls")),
    # URLs de la app accounts (login, dashboard, perfil)
    path("", include("apps.accounts.urls")),
    # Redirección raíz al login
    path("", RedirectView.as_view(pattern_name="login", permanent=False)),
]

# URLs de desarrollo (solo en DEBUG)
if settings.DEBUG:
    try:
        import debug_toolbar

        urlpatterns = [
            path("__debug__/", include(debug_toolbar.urls)),
        ] + urlpatterns
    except ImportError:
        pass
