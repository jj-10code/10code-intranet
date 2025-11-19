"""
Signals del módulo de Autenticación y Usuarios.

Maneja eventos de autenticación para procesamiento adicional.
"""

import logging

from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in

from apps.accounts.services import AuthService

logger = logging.getLogger(__name__)


@receiver(user_logged_in)
def on_user_logged_in(sender, request, user, **kwargs):
    """
    Signal disparado cuando un usuario inicia sesión.

    Procesa el login exitoso (auditoría, actualización de datos).
    """
    # Procesar login exitoso
    try:
        AuthService.handle_successful_google_login(request=request, user=user)
    except Exception as e:
        logger.error(f"Error procesando login de {user.email}: {e}", exc_info=True)



