"""
Configuración de la app Accounts.
"""

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """Configuración de la aplicación de autenticación y usuarios."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.accounts"
    verbose_name = "Autenticación y Usuarios"

    def ready(self):
        """
        Importar signals cuando la app esté lista.
        """
        import apps.accounts.signals  # noqa: F401
