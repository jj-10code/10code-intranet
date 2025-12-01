"""
Services del módulo de Autenticación y Usuarios.

Contienen toda la lógica de negocio (WRITE operations).
Siguen el patrón Service Layer para fat services / thin views.
"""

import logging
from typing import Optional

from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
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



class RoleService:
    """
    Servicio de gestión de roles.

    Maneja la asignación y revocación de roles.
    """

    @staticmethod
    @transaction.atomic
    def assign_role_to_user(
        *, user: User, role_code: str, assigned_by: Optional[User] = None
    ) -> UserRole:
        """
        Asigna un rol a un usuario.

        Args:
            user: Usuario al que asignar el rol
            role_code: Código del rol a asignar
            assigned_by: Usuario que realiza la asignación (opcional)

        Returns:
            UserRole creado o existente

        Raises:
            Role.DoesNotExist: Si el rol no existe
        """
        role = Role.objects.get(code=role_code)

        user_role, created = UserRole.objects.get_or_create(
            user=user,
            role=role,
            defaults={"assigned_by": assigned_by},
        )

        if created:
            # Registrar en AuditLog
            AuditLog.objects.create(
                user=assigned_by,
                action=AuditLog.Action.ROLE_ASSIGNED,
                resource_type="User",
                resource_id=user.id,
                metadata={
                    "role_code": role.code,
                    "role_name": role.name,
                    "assigned_to": user.email,
                },
            )
            logger.info(f"Rol '{role.code}' asignado a {user.email} por {assigned_by}")
        else:
            logger.info(f"Usuario {user.email} ya tenía el rol '{role.code}'")

        return user_role


class UserService:
    """
    Servicio de gestión de usuarios.

    Maneja operaciones CRUD de usuarios.
    """

    @staticmethod
    @transaction.atomic
    def create_user_manually(
        *,
        email: str,
        first_name: str,
        last_name: str,
        date_of_birth: timezone.datetime.date,
        roles: list[str],
        created_by: User,
    ) -> User:
        """
        Crear usuario manualmente por administrador.

        Args:
            email: Email @10code.es
            first_name: Nombre
            last_name: Apellido
            date_of_birth: Fecha de nacimiento (obligatoria)
            roles: Lista de códigos de roles a asignar
            created_by: Usuario que crea

        Returns:
            Usuario creado con is_active=False

        Raises:
            ValidationError: si email no es @10code.es o ya existe, o edad < 16
            PermissionDenied: si created_by no tiene permiso
        """
        # 1. Verificar permiso del creador
        if not created_by.has_perm("accounts.add_user"):
             from django.core.exceptions import PermissionDenied
             raise PermissionDenied("No tiene permiso para crear usuarios.")

        # 2. Validar dominio
        if not AuthService.validate_email_domain(email):
            raise ValidationError("El email debe pertenecer al dominio @10code.es")

        # 3. Validar unicidad
        if User.objects.filter(email=email).exists():
            raise ValidationError("Ya existe un usuario con este email.")

        # 4. Validar edad
        today = timezone.now().date()
        age = (
            today.year
            - date_of_birth.year
            - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
        )
        if age < 16:
            raise ValidationError("El usuario debe tener al menos 16 años.")

        # 5. Crear usuario
        user = User.objects.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            is_active=False,
        )

        # 6. Asignar roles
        for role_code in roles:
            RoleService.assign_role_to_user(
                user=user, role_code=role_code, assigned_by=created_by
            )

        # 7. Audit Log
        AuditLog.objects.create(
            user=created_by,
            action=AuditLog.Action.USER_CREATED,
            resource_type="User",
            resource_id=user.id,
            metadata={
                "new_user_email": user.email,
                "roles_assigned": roles,
                "manual_creation": True,
            },
        )

        logger.info(f"Usuario creado manualmente: {user.email} por {created_by.email}")

        return user

    @staticmethod
    @transaction.atomic
    def update_user_profile(
        *,
        user: User,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        avatar_url: Optional[str] = None,
        avatar: Optional[Any] = None,
    ) -> User:
        """
        Actualiza perfil básico del usuario.

        Args:
            user: Usuario a actualizar
            first_name: Nombre (opcional)
            last_name: Apellidos (opcional)
            avatar_url: URL del avatar (opcional, para externos)
            avatar: Archivo de imagen (opcional, para subidas)

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

        if avatar is not None:
            # Si se sube una nueva imagen, la guardamos en el campo avatar
            user.avatar = avatar
            updated_fields.append("avatar")
            # Opcional: Limpiar avatar_url externo si se prefiere la imagen local
            # user.avatar_url = None 
            # updated_fields.append("avatar_url")
        elif avatar_url is not None:
            # Si se pasa una URL (ej: Google), la guardamos en avatar_url
            user.avatar_url = avatar_url
            updated_fields.append("avatar_url")

        if updated_fields:
            user.save(update_fields=updated_fields)
            logger.info(f"Perfil actualizado: {user.email}, campos={updated_fields}")

        return user

    @staticmethod
    @transaction.atomic
    def deactivate_user(*, user: User, deactivated_by: User, reason: str) -> User:
        """
        Desactiva un usuario (soft delete).

        Args:
            user: Usuario a desactivar
            deactivated_by: Usuario que realiza la acción
            reason: Motivo de desactivación

        Returns:
            Usuario desactivado

        Raises:
            PermissionError: si deactivated_by no tiene permiso
        """
        # 1. Verificar permiso
        if not deactivated_by.has_perm("accounts.delete_user"):
            raise PermissionError("No tiene permiso para desactivar usuarios.")

        # 2. Marcar is_active = False (idempotente)
        if user.is_active:
            user.is_active = False
            user.save(update_fields=["is_active"])
            logger.info(f"Usuario desactivado: {user.email} por {deactivated_by.email}")
        else:
            logger.info(f"Usuario {user.email} ya estaba desactivado")

        # 3. Registrar en AuditLog (siempre, incluso si ya estaba desactivado)
        AuditLog.objects.create(
            user=deactivated_by,
            action=AuditLog.Action.USER_DEACTIVATED,
            resource_type="User",
            resource_id=user.id,
            metadata={
                "deactivated_user_email": user.email,
                "reason": reason,
            },
        )

        # 4. Nota: Sesiones se invalidan via ActivityTrackingMiddleware

        return user
