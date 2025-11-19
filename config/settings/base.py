# config/settings/base.py

import logging
import os
from pathlib import Path

import environ

from config.secrets import get_environment, read_secret, validate_secret_key

# Construcción de paths dentro del proyecto como BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Inicializar variables de entorno
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False),
    DATABASE_CONN_MAX_AGE=(int, 60)
)

environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# Configurar logging
logger = logging.getLogger(__name__)

# Detectar entorno actual
ENVIRONMENT = get_environment()

# Cargar SECRET_KEY desde archivos o env vars
SECRET_KEY = read_secret("django_secret_key", required=True)

# Validar SECRET_KEY según el entorno
if not validate_secret_key(SECRET_KEY, environment=ENVIRONMENT):
    raise ValueError(
        f"SECRET_KEY no cumple requisitos de seguridad para entorno '{ENVIRONMENT}'. "
        f"Genera una nueva clave segura con: python -c 'from django.core.management.utils "
        f"import get_random_secret_key; print(get_random_secret_key())'"
    )

# SECURITY WARNING: No dejes esto en True en producción!
DEBUG = env("DEBUG")

# Definimos las aplicaciones instaladas
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",  # Requerido por allauth
]

THIRD_PARTY_APPS = [
    # Inertia.js
    "inertia",
    # REST Framework
    "rest_framework",
    "corsheaders",
    # Allauth
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    # Celery
    "django_celery_beat",
]

LOCAL_APPS = [
    "apps.core",
    "apps.accounts",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# Configuración de middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",  # Habilitar CORS middleware
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Sirve archivos estáticos en producción
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DATABASE_NAME", default="10code_intranet"),
        "USER": env("DATABASE_USER", default="postgres"),
        "PASSWORD": read_secret("db_password", required=False, default="postgres"),
        "HOST": env("DATABASE_HOST", default="localhost"),
        "PORT": env("DATABASE_PORT", default="5432"),
        "CONN_MAX_AGE": env("DATABASE_CONN_MAX_AGE", default=60),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "es-ES"

TIME_ZONE = "Europe/Madrid"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = []

# WhiteNoise configuration
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Media files
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ========================================
# AUTH CONFIGURATION
# ========================================

# Usar modelo de Usuario personalizado
AUTH_USER_MODEL = "accounts.User"

# Sitio ID requerido por django-allauth
SITE_ID = 1

# Configuración de django-allauth
AUTHENTICATION_BACKENDS = [
    # Backend de Django por defecto (permite superuser login)
    "django.contrib.auth.backends.ModelBackend",
    # Backend de allauth para autenticación con terceros
    "allauth.account.auth_backends.AuthenticationBackend",
]

# Configuración de allauth
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = "none"  # Google ya verifica el email
ACCOUNT_USER_MODEL_USERNAME_FIELD = "username"
ACCOUNT_USER_MODEL_EMAIL_FIELD = "email"

# Configuración de Social Account
SOCIALACCOUNT_AUTO_SIGNUP = True  # Crear usuario automáticamente
SOCIALACCOUNT_EMAIL_VERIFICATION = "none"  # Google ya verifica
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_EMAIL_AUTHENTICATION = True  # Confía en emails verificados por Google
SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT = True
SOCIALACCOUNT_LOGIN_ON_GET = False  # Seguridad: evita login en GET
SOCIALACCOUNT_ADAPTER = "apps.accounts.adapters.SocialAccountAdapter"  # Custom adapter

# Configuración del proveedor Google
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
            "hd": "10code.es",  # Filtra el selector de cuentas
        },
        "FETCH_USERINFO": True,
        "OAUTH_PKCE_ENABLED": True,
    }
}

# URLs de redirección después de login/logout
LOGIN_REDIRECT_URL = "/dashboard/"
ACCOUNT_LOGOUT_REDIRECT_URL = "/login/"

# ========================================
# CELERY CONFIGURATION
# ========================================

# Broker y Backend
CELERY_BROKER_URL = env("CELERY_BROKER_URL", default="redis://localhost:6379/1")
CELERY_RESULT_BACKEND = CELERY_BROKER_URL

# Serialización
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"

# Zona horaria
CELERY_TIMEZONE = TIME_ZONE

# Configuración de tareas
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60  # 30 minutos
CELERY_TASK_SOFT_TIME_LIMIT = 25 * 60  # 25 minutos (warning antes del hard limit)
