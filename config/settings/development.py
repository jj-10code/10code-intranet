# config/settings/development.py
from .base import *  # noqa: F403

# === HOSTS PERMITIDOS ===
ALLOWED_HOSTS = ["*"]

# === APLICACIONES ADICIONALES PARA DESARROLLO ===
INSTALLED_APPS += [  # noqa: F405
    "django_extensions",
    "debug_toolbar",
]

# === MIDDLEWARE ADICIONAL PARA DESARROLLO ===
MIDDLEWARE += [  # noqa: F405
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

# === CONFIGURACIÓN DE DEBUG TOOLBAR ===
INTERNAL_IPS = ["127.0.0.1", "localhost"]

# CORS permisivo en desarrollo
CORS_ALLOW_ALL_ORIGINS = True
