"""
Configuración de la app Accounts.
"""

import logging

from django.apps import AppConfig

logger = logging.getLogger(__name__)


class AccountsConfig(AppConfig):
    """Configuración de la aplicación de autenticación y usuarios."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.accounts"
    verbose_name = "Autenticación y Usuarios"

    def ready(self):
        """
        Importar signals cuando la app esté lista.
        """
        # Conectar signal para verificar Social Apps después de migraciones
        from django.db.models.signals import post_migrate

        import apps.accounts.signals  # noqa: F401

        post_migrate.connect(self._check_social_apps, sender=self)

    def _check_social_apps(self, **kwargs):
        """
        Verifica que las aplicaciones sociales estén configuradas correctamente.
        Se ejecuta después de las migraciones.
        """
        try:
            from allauth.socialaccount.models import SocialApp

            google_apps = SocialApp.objects.filter(provider="google")
            if not google_apps.exists():
                logger.warning(
                    "⚠️  Google SocialApp no está configurada. "
                    "Ejecuta 'python scripts/setup_social_app.py' para configurar OAuth. "
                    "Los usuarios no podrán iniciar sesión con Google hasta que se configure."
                )
            else:
                app = google_apps.first()
                logger.info(
                    f"✅ Google SocialApp configurada: {app.name} (ID: {app.client_id[:10]}...)"
                )
        except Exception as e:
            logger.error(f"❌ Error verificando Social Apps: {e}")
