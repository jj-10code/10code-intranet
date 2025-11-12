# config/settings/production.py
from .base import *  # noqa: F403

# Configuraciones específicas para producción
ALLOWED_HOSTS = list(env("ALLOWED_HOSTS", default="ocalhost,127.0.0.1").split(","))  # noqa: F405

SECURE_SSL_REDIRECT = env("SECURE_SSL_REDIRECT", default="True") == "True"  # noqa: F405
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

# CORS específico
CORS_ALLOWED_ORIGINS = (
    env("CORS_ALLOWED_ORIGINS", default="").split(",") if env("CORS_ALLOWED_ORIGINS") else []  # noqa: F405
)

# Logging a stdout (Docker-friendly)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": env("LOG_LEVEL", default="INFO"),  # noqa: F405
    },
}
# Otras configuraciones de producción pueden ir aquí

# Configuración de caché para producción (ejemplo con Redis)
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env("REDIS_URL", default="redis://localhost:6379/0"),  # noqa: F405
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

# Configuración de Celery para producción
CELERY_BROKER_URL = env("CELERY_BROKER_URL", default="redis://localhost:6379/1")  # noqa: F405
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE  # noqa: F405
