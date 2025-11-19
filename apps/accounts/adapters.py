"""
Adaptadores personalizados para django-allauth.

Incluye validaciones específicas de negocio para autenticación.
"""

from allauth.core.exceptions import ImmediateHttpResponse
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.shortcuts import render


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Adaptador personalizado para Social Account.

    Valida que solo usuarios con email @10code.es puedan autenticarse.
    Proporciona mejores mensajes de error para problemas de configuración.
    """

    ALLOWED_DOMAIN = "10code.es"

    def get_app(self, request, provider, client_id=None, **kwargs):
        """
        Obtiene la aplicación social configurada.

        Proporciona mejor manejo de errores cuando la app no existe.
        """
        try:
            return super().get_app(request, provider, client_id=client_id, **kwargs)
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(
                f"SocialApp para provider '{provider}' no está configurada. "
                f"Ejecuta 'python scripts/setup_social_app.py' para configurar las credenciales de Google OAuth. "
                f"Asegúrate de que las credenciales estén en secrets/google_client_id.txt y secrets/google_client_secret.txt"
            )

    def pre_social_login(self, request, sociallogin):
        """
        Hook llamado antes de procesar el login social.

        Valida que el email sea del dominio corporativo @10code.es.
        """
        email = sociallogin.account.extra_data.get("email", "")

        if not email.endswith(f"@{self.ALLOWED_DOMAIN}"):
            raise PermissionDenied(
                f"Solo se permiten usuarios con email @{self.ALLOWED_DOMAIN}. "
                f"Tu email '{email}' no está autorizado."
            )

        # IMPORTANTE: También valida el claim 'hd' del ID token
        extra_data = sociallogin.account.extra_data
        hd = extra_data.get("hd", "")

        if hd != "10code.es":
            raise ImmediateHttpResponse(
                render(
                    request,
                    "account/domain_restricted.html",
                    {
                        "email": email,
                        "allowed_domain": "10code.es",
                        "error": "Domain verification failed",
                    },
                )
            )

    def populate_user(self, request, sociallogin, data):
        """
        Personaliza cómo se popula el User desde datos de Google.
        """
        user = super().populate_user(request, sociallogin, data)

        # Extraer datos adicionales de Google
        extra_data = sociallogin.account.extra_data

        # Asignar nombre y apellidos
        user.first_name = extra_data.get("given_name", "")
        user.last_name = extra_data.get("family_name", "")

        # Asignar avatar URL
        user.avatar_url = extra_data.get("picture", "")

        return user

    def save_user(self, request, sociallogin, form=None):
        """
        Guarda el usuario y crea el GoogleProfile asociado.
        """
        user = super().save_user(request, sociallogin, form)

        # Importación local para evitar circular import
        from apps.accounts.models import GoogleProfile

        # Crear GoogleProfile si no existe
        google_id = sociallogin.account.extra_data.get("sub") or sociallogin.account.uid
        GoogleProfile.objects.update_or_create(
            user=user,
            defaults={
                "google_id": google_id,
                "email": sociallogin.account.extra_data.get("email", ""),
                "raw_data": sociallogin.account.extra_data,
            },
        )

        return user
