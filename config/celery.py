"""
Configuración de Celery para 10Code Intranet.

Para más información sobre configuración de Celery con Django:
https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html
"""

import os

from celery import Celery

# Establecer el módulo de settings por defecto para Celery
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")

# Crear la aplicación Celery
app = Celery("10code_intranet")

# Cargar configuración desde Django settings con namespace 'CELERY'
# Esto significa que todas las configuraciones relacionadas con Celery
# deben tener el prefijo CELERY_ en settings.py
app.config_from_object("django.conf:settings", namespace="CELERY")

# Autodiscovery de tareas en todas las apps instaladas
# Busca archivos tasks.py en cada app Django
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    """Tarea de debug para verificar que Celery funciona."""
    print(f"Request: {self.request!r}")
