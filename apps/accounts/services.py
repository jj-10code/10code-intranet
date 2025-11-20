"""
Services del módulo de Autenticación y Usuarios.

Contienen toda la lógica de negocio (WRITE operations).
Siguen el patrón Service Layer para fat services / thin views.
"""

import logging
from typing import Optional

from django.contrib.auth import authenticate, login, logout
from django.db import transaction
from django.http import HttpRequest
from django.utils import timezone

from apps.accounts.models import AuditLog, Role, User, UserRole

logger = logging.getLogger(__name__)


class AuthService:
    """
    Servicio de autenticación.

    Maneja login con Google OAuth, logout y auditoría.
    """

    @staticmethod
    def get_client_ip(request: HttpRequest) -> str:
        """Obtiene la IP del cliente desde la request."""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip

    @staticmethod
    def validate_email_domain(email: str) -> bool:
        """
        Valida que el email pertenezca al dominio corporativo.

        Args:
            email: Email a validar

        Returns:
            True si es válido, False si no
        """
        return email.endswith("@10code.es")

    @staticmethod
    @transaction.atomic
    def handle_successful_google_login(
        *, request: HttpRequest, user: User
    ) -> User:
        """
        Procesa login exitoso con Google OAuth.

        Actualiza last_login, crea AuditLog y asigna rol 'employee' si es primer login.

        Args:
            request: HTTP Request object
            user: Usuario autenticado

        Returns:
            Usuario procesado

        Raises:
            Exception: Si hay error en el procesamiento
        """
        # Actualizar last_login
        user.last_login = timezone.now()
        user.save(update_fields=["last_login"])

        # Verificar si es primer login (nuevo usuario)
        is_first_login = user.date_joined.date() == timezone.now().date()

        if is_first_login:
            # Asignar rol 'employee' por defecto
            try:
                employee_role = Role.objects.get(code="employee")
                UserRole.objects.get_or_create(
                    user=user,
                    role=employee_role,
                    defaults={"assigned_by": None},  # Auto-asignado
                )
                logger.info(f"Rol 'employee' asignado a nuevo usuario: {user.email}")
            except Role.DoesNotExist:
                logger.error("Rol 'employee' no existe. Verifica fixtures de roles.")

        # Registrar login en AuditLog
        AuditLog.objects.create(
            user=user,
            action=AuditLog.Action.LOGIN,
            resource_type="User",
            resource_id=user.id,
            metadata={
                "is_first_login": is_first_login,
                "provider": "google",
            },
            ip_address=AuthService.get_client_ip(request),
        )

        logger.info(f"Login exitoso: {user.email} (first_login={is_first_login})")

        return user

    @staticmethod
    @transaction.atomic
    def logout_user(*, request: HttpRequest, user: User) -> None:
        """
        Cierra sesión del usuario.

        Registra logout en AuditLog y limpia sesión.

        Args:
            request: HTTP Request object
            user: Usuario a desloguear
        """
        # Registrar logout en AuditLog
        AuditLog.objects.create(
            user=user,
            action=AuditLog.Action.LOGOUT,
            resource_type="User",
            resource_id=user.id,
            metadata={},
            ip_address=AuthService.get_client_ip(request),
        )

        logger.info(f"Logout exitoso: {user.email}")

        # Cerrar sesión Django
        logout(request)

    @staticmethod
    def log_failed_login(*, request: HttpRequest, email: Optional[str] = None) -> None:
        """
        Registra intento de login fallido.

        Args:
            request: HTTP Request object
            email: Email del intento (si está disponible)
        """
        AuditLog.objects.create(
            user=None,  # No hay usuario asociado
            action=AuditLog.Action.LOGIN_FAILED,
            metadata={
                "email": email or "desconocido",
                "reason": "Dominio no autorizado o credenciales inválidas",
            },
            ip_address=AuthService.get_client_ip(request),
        )

        logger.warning(
            f"Intento de login fallido: email={email}, ip={AuthService.get_client_ip(request)}"
        )


class UserService:
    """
    Servicio de gestión de usuarios.

    Maneja operaciones CRUD de usuarios.
    """

    @staticmethod
    @transaction.atomic
    def update_user_profile(
        *,
        user: User,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        avatar_url: Optional[str] = None,
    ) -> User:
        """
        Actualiza perfil básico del usuario.

        Args:
            user: Usuario a actualizar
            first_name: Nombre (opcional)
            last_name: Apellidos (opcional)
            avatar_url: URL del avatar (opcional)

        Returns:
            Usuario actualizado
        """
        updated_fields = []

        if first_name is not None:
            user.first_name = first_name
            updated_fields.append("first_name")

        if last_name is not None:
            user.last_name = last_name
            updated_fields.append("last_name")

        if avatar_url is not None:
            user.avatar_url = avatar_url
            updated_fields.append("avatar_url")

        if updated_fields:
            user.save(update_fields=updated_fields)
            logger.info(f"Perfil actualizado: {user.email}, campos={updated_fields}")

        return user

    @staticmethod
    @transaction.atomic
    def deactivate_user(*, user: User, deactivated_by: User) -> User:
        """
        Desactiva un usuario.

        Args:
            user: Usuario a desactivar
            deactivated_by: Usuario que realiza la acción

        Returns:
            Usuario desactivado
        """
        user.is_active = False
        user.save(update_fields=["is_active"])

        # Registrar en AuditLog
        AuditLog.objects.create(
            user=deactivated_by,
            action=AuditLog.Action.USER_DEACTIVATED,
            resource_type="User",
            resource_id=user.id,
            metadata={
                "deactivated_user_email": user.email,
            },
        )

        logger.info(f"Usuario desactivado: {user.email} por {deactivated_by.email}")

        return user
