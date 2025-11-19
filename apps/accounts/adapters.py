"""
Adaptadores personalizados para django-allauth.

Incluye validaciones específicas de negocio para autenticación.
"""

from django.core.exceptions import PermissionDenied

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Adaptador personalizado para Social Account.

    Valida que solo usuarios con email @10code.es puedan autenticarse.
    """

    ALLOWED_DOMAIN = "10code.es"

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
        hd = extra_data.get('hd', '')
        
        if hd != '10code.es':
            raise ImmediateHttpResponse(
                render(request, 'account/domain_restricted.html', {
                    'email': email,
                    'allowed_domain': '10code.es',
                    'error': 'Domain verification failed'
                })
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
