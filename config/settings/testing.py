from .base import *

DEBUG = False
SECRET_KEY = "testing-secret-key"

# Use in-memory database for speed
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# Faster password hashing
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

# Disable email sending
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# Disable celery
CELERY_TASK_ALWAYS_EAGER = True

# Use local memory cache for testing
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}

# Use cache-based sessions (will use LocMemCache now)
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
