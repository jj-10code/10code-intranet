"""
Signals del módulo de Autenticación y Usuarios.

Maneja eventos de autenticación para procesamiento adicional.
"""

import logging

from django.dispatch import receiver

from allauth.socialaccount.signals import pre_social_login, social_account_added

from apps.accounts.services import AuthService

logger = logging.getLogger(__name__)


@receiver(social_account_added)
def on_social_account_added(sender, request, sociallogin, **kwargs):
    """
    Signal disparado cuando se conecta una cuenta social exitosamente.

    Procesa el login exitoso con Google OAuth.
    """
    user = sociallogin.user

    # Procesar login exitoso
    try:
        AuthService.handle_successful_google_login(request=request, user=user)
    except Exception as e:
        logger.error(f"Error procesando login de {user.email}: {e}", exc_info=True)


@receiver(pre_social_login)
def on_pre_social_login(sender, request, sociallogin, **kwargs):
    """
    Signal disparado antes de procesar el login social.

    Aquí podemos realizar validaciones adicionales.
    """
    # La validación de dominio @10code.es ya se maneja en SocialAccountAdapter.pre_social_login
    pass
