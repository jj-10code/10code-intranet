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
