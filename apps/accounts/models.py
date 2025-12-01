"""
Modelos del módulo de Autenticación y Usuarios.

Incluye:
- User: Modelo de usuario personalizado
- GoogleProfile: Perfil OAuth de Google
- Role: Roles del sistema
- UserRole: Relación usuarios-roles
- Permission: Permisos granulares
- AuditLog: Registro de auditoría
"""

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from apps.core.models import TimestampedModel


class UserManager(BaseUserManager):
    """Manager personalizado para User que usa email como username."""

    def create_user(self, email, password=None, **extra_fields):
        """
        Crea y guarda un usuario con el email y password dados.
        """
        if not email:
            raise ValueError("El email es obligatorio")

        email = self.normalize_email(email)
        user = self.model(email=email, username=email, **extra_fields)

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()  # Para usuarios OAuth

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Crea y guarda un superusuario.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser debe tener is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser debe tener is_superuser=True")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Modelo de Usuario personalizado.

    Usa email como identificador principal en lugar de username.
    Información personal mínima para cumplir RGPD.
    """

    # Override username para usar email
    username = models.CharField(
        max_length=150,
        unique=True,
        help_text="Username autogenerado desde email",
        editable=False,
    )
    email = models.EmailField(
        unique=True,
        verbose_name="Email corporativo",
        help_text="Email @10code.es para autenticación",
    )

    # Información básica (extraída de Google)
    first_name = models.CharField(max_length=150, verbose_name="Nombre")
    last_name = models.CharField(max_length=150, verbose_name="Apellidos")
    date_of_birth = models.DateField(
        null=True, blank=True, verbose_name="Fecha de nacimiento"
    )

    # Avatar
    avatar = models.ImageField(
        upload_to="avatars/",
        blank=True,
        null=True,
        verbose_name="Avatar (Imagen)",
        help_text="Imagen subida por el usuario",
    )
    avatar_url = models.URLField(
        blank=True, null=True, verbose_name="Avatar (URL)", help_text="URL del avatar de Google"
    )

    # Campos de activación
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    is_staff = models.BooleanField(default=False, verbose_name="Staff")

    # Timestamps
    date_joined = models.DateTimeField(default=timezone.now, verbose_name="Fecha de registro")
    last_login = models.DateTimeField(null=True, blank=True, verbose_name="Último login")

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        db_table = "users"
        ordering = ["-date_joined"]
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self) -> str:
        return f"{self.get_full_name()} ({self.email})"

    def get_full_name(self) -> str:
        """Retorna nombre completo del usuario."""
        return f"{self.first_name} {self.last_name}".strip()

    def has_role(self, role_code: str) -> bool:
        """Verifica si el usuario tiene un rol específico."""
        return self.user_roles.filter(role__code=role_code).exists()


class GoogleProfile(TimestampedModel):
    """
    Perfil de Google OAuth vinculado a un usuario.

    Almacena información mínima necesaria de la cuenta Google.
    """

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="google_profile", verbose_name="Usuario"
    )
    google_id = models.CharField(
        max_length=255, unique=True, verbose_name="Google ID", help_text="ID único de Google"
    )
    email = models.EmailField(
        verbose_name="Email de Google", help_text="Email verificado de Google"
    )
    raw_data = models.JSONField(
        default=dict, blank=True, verbose_name="Datos raw", help_text="Datos extra del perfil"
    )

    class Meta:
        verbose_name = "Perfil de Google"
        verbose_name_plural = "Perfiles de Google"
        db_table = "google_profiles"
        indexes = [
            models.Index(fields=["google_id"]),
        ]

    def __str__(self) -> str:
        return f"Google Profile: {self.user.email}"


class Role(TimestampedModel):
    """
    Roles del sistema.

    Define grupos de permisos que se pueden asignar a usuarios.
    Soporta herencia de roles (parent_role).
    """

    code = models.SlugField(
        max_length=50, unique=True, verbose_name="Código", help_text="Código único del rol"
    )
    name = models.CharField(max_length=100, verbose_name="Nombre", help_text="Nombre descriptivo")
    description = models.TextField(blank=True, verbose_name="Descripción")
    parent_role = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="child_roles",
        verbose_name="Rol padre",
        help_text="Rol del que hereda permisos",
    )
    is_system = models.BooleanField(
        default=False,
        verbose_name="Rol del sistema",
        help_text="Roles predefinidos no editables",
    )

    class Meta:
        verbose_name = "Rol"
        verbose_name_plural = "Roles"
        db_table = "roles"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class UserRole(TimestampedModel):
    """
    Tabla de unión entre Users y Roles (Many-to-Many con metadata).

    Permite asignar múltiples roles a un usuario con auditoría.
    """

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_roles", verbose_name="Usuario"
    )
    role = models.ForeignKey(
        Role, on_delete=models.CASCADE, related_name="role_users", verbose_name="Rol"
    )
    assigned_at = models.DateTimeField(
        default=timezone.now, verbose_name="Asignado el", help_text="Fecha de asignación"
    )
    assigned_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="roles_assigned",
        verbose_name="Asignado por",
        help_text="Usuario que asignó el rol",
    )

    class Meta:
        verbose_name = "Rol de Usuario"
        verbose_name_plural = "Roles de Usuarios"
        db_table = "user_roles"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "role"], name="unique_user_role"
            ),
        ]
        indexes = [
            models.Index(fields=["user", "role"]),
        ]

    def __str__(self) -> str:
        return f"{self.user.email} - {self.role.name}"


class Permission(models.Model):
    """
    Permisos granulares por rol.

    Formato: app.action_model (ej: projects.add_project)
    """

    role = models.ForeignKey(
        Role, on_delete=models.CASCADE, related_name="permissions", verbose_name="Rol"
    )
    permission_code = models.CharField(
        max_length=100,
        verbose_name="Código de permiso",
        help_text="Formato: app.action_model (ej: projects.add_project)",
    )

    class Meta:
        verbose_name = "Permiso"
        verbose_name_plural = "Permisos"
        db_table = "permissions"
        constraints = [
            models.UniqueConstraint(
                fields=["role", "permission_code"], name="unique_role_permission"
            ),
        ]
        indexes = [
            models.Index(fields=["role", "permission_code"]),
        ]

    def __str__(self) -> str:
        return f"{self.role.code}: {self.permission_code}"


class AuditLog(TimestampedModel):
    """
    Registro de auditoría de acciones en el sistema.

    Almacena eventos importantes para trazabilidad y cumplimiento RGPD.
    Retención mínima: 4 años (normativa española).
    """

    class Action(models.TextChoices):
        LOGIN = "login", "Login"
        LOGOUT = "logout", "Logout"
        LOGIN_FAILED = "login_failed", "Login fallido"
        USER_CREATED = "user_created", "Usuario creado"
        USER_UPDATED = "user_updated", "Usuario actualizado"
        USER_DEACTIVATED = "user_deactivated", "Usuario desactivado"
        ROLE_ASSIGNED = "role_assigned", "Rol asignado"
        ROLE_REMOVED = "role_removed", "Rol removido"
        PERMISSION_CHANGE = "permission_change", "Cambio de permisos"

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_logs",
        verbose_name="Usuario",
        help_text="Usuario que realizó la acción (null para eventos del sistema)",
    )
    action = models.CharField(
        max_length=50, choices=Action.choices, verbose_name="Acción", db_index=True
    )
    resource_type = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Tipo de recurso",
        help_text="Ej: User, Role, Project",
    )
    resource_id = models.BigIntegerField(
        null=True, blank=True, verbose_name="ID del recurso", help_text="ID del objeto afectado"
    )
    metadata = models.JSONField(
        default=dict, blank=True, verbose_name="Metadatos", help_text="Información adicional JSON"
    )
    ip_address = models.GenericIPAddressField(
        null=True, blank=True, verbose_name="Dirección IP", help_text="IP del cliente"
    )
    timestamp = models.DateTimeField(
        default=timezone.now, db_index=True, verbose_name="Fecha y hora"
    )

    class Meta:
        verbose_name = "Log de Auditoría"
        verbose_name_plural = "Logs de Auditoría"
        db_table = "audit_logs"
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["user", "timestamp"]),
            models.Index(fields=["action", "timestamp"]),
        ]

    def __str__(self) -> str:
        user_str = self.user.email if self.user else "Sistema"
        return f"{self.timestamp.strftime('%Y-%m-%d %H:%M')} - {user_str}: {self.get_action_display()}"
