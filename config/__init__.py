"""
Configuración del paquete config.

Importa la aplicación Celery para que Django la cargue automáticamente.
"""

from .celery import app as celery_app

__all__ = ("celery_app",)
