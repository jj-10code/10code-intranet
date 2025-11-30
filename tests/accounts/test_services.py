"""
Tests para los servicios del módulo accounts.

Verifica la lógica de negocio de autenticación, usuarios y roles.
"""

import pytest
from unittest.mock import Mock
from django.utils import timezone
from apps.accounts.services import AuthService, UserService, RoleService
from apps.accounts.models import AuditLog, UserRole
from tests.factories import UserFactory, RoleFactory


@pytest.mark.integration
@pytest.mark.django_db
class TestAuthService:
    """Tests para el servicio de autenticación."""

    def test_handle_successful_google_login_first_time(self):
        """Verifica el primer login con Google."""
        user = UserFactory(last_login=None)
        request = Mock()
        request.META = {"REMOTE_ADDR": "127.0.0.1"}
        
        # Ensure employee role exists
        RoleFactory(code="employee")

        AuthService.handle_successful_google_login(request=request, user=user)

        user.refresh_from_db()
        assert user.last_login is not None
        assert user.has_role("employee")
        assert AuditLog.objects.filter(user=user, action=AuditLog.Action.LOGIN).exists()

    def test_handle_successful_google_login_returning_user(self):
        """Verifica login recurrente con Google."""
        user = UserFactory(last_login=timezone.now(), date_joined=timezone.now() - timezone.timedelta(days=1))
        request = Mock()
        request.META = {"REMOTE_ADDR": "127.0.0.1"}
        
        # Ensure employee role exists
        RoleFactory(code="employee")

        AuthService.handle_successful_google_login(request=request, user=user)

        # No se debe re-asignar el rol si ya existe (o si no es nuevo usuario)
        # Nota: La lógica actual parece no asignar rol si no es first_time
        assert not UserRole.objects.filter(user=user, role__code="employee").exists()
        assert AuditLog.objects.filter(user=user, action=AuditLog.Action.LOGIN).exists()

    def test_logout_user(self):
        """Verifica el logout y su auditoría."""
        user = UserFactory()
        request = Mock()
        request.META = {"REMOTE_ADDR": "127.0.0.1"}
        request.session = Mock()

        AuthService.logout_user(request=request, user=user)

        assert AuditLog.objects.filter(user=user, action=AuditLog.Action.LOGOUT).exists()

    def test_log_failed_login(self):
        """Verifica el registro de logins fallidos."""
        request = Mock()
        request.META = {"REMOTE_ADDR": "127.0.0.1"}

        AuthService.log_failed_login(request=request, email="fail@example.com")

        assert AuditLog.objects.filter(action=AuditLog.Action.LOGIN_FAILED).exists()

    @pytest.mark.unit
    @pytest.mark.parametrize("email,expected", [
        ("user@10code.es", True),
        ("admin@10code.es", True),
        ("user@gmail.com", False),
        ("user@other.com", False),
        ("invalid-email", False),
        ("", False),
    ])
    def test_validate_email_domain(self, email, expected):
        """Verifica la validación de dominios de email."""
        assert AuthService.validate_email_domain(email) == expected


@pytest.mark.integration
@pytest.mark.django_db
class TestUserService:
    """Tests para el servicio de gestión de usuarios."""

    def test_update_user_profile(self, user_factory):
        """Verifica la actualización de perfil."""
        user = user_factory()
        
        UserService.update_user_profile(
            user=user,
            first_name="NewName",
            last_name="NewLast",
            avatar_url="http://new.url/avatar.jpg"
        )
        
        user.refresh_from_db()
        assert user.first_name == "NewName"
        assert user.last_name == "NewLast"
        assert user.avatar_url == "http://new.url/avatar.jpg"

    def test_deactivate_user_success(self, user_factory):
        """Verifica la desactivación exitosa de un usuario."""
        user = user_factory(is_active=True)
        admin = user_factory(is_staff=True)
        # Mock permissions
        admin.has_perm = Mock(return_value=True)
        
        UserService.deactivate_user(
            user=user, 
            deactivated_by=admin,
            reason="Baja temporal por excedencia"
        )
        
        user.refresh_from_db()
        assert user.is_active is False
        
        # Verify audit log with reason
        audit = AuditLog.objects.filter(
            action=AuditLog.Action.USER_DEACTIVATED,
            resource_id=user.id
        ).first()
        assert audit is not None
        assert audit.metadata["reason"] == "Baja temporal por excedencia"
        assert audit.metadata["deactivated_user_email"] == user.email

    def test_deactivate_user_without_permission(self, user_factory):
        """Verifica que se requiere permiso para desactivar."""
        user = user_factory(is_active=True)
        regular_user = user_factory(is_staff=False)
        # Mock permissions to False
        regular_user.has_perm = Mock(return_value=False)
        
        from django.core.exceptions import PermissionDenied
        
        # Nota: El servicio lanza PermissionError o PermissionDenied dependiendo de la implementación.
        # Ajustamos a lo que vimos en el código original (PermissionError parece ser usado en el test original, 
        # pero PermissionDenied es más Django-friendly. Asumimos PermissionError por el test anterior).
        with pytest.raises(PermissionError, match="No tiene permiso"):
            UserService.deactivate_user(
                user=user,
                deactivated_by=regular_user,
                reason="Intento no autorizado"
            )
        
        # User should still be active
        user.refresh_from_db()
        assert user.is_active is True

    def test_deactivate_user_idempotent(self, user_factory):
        """Verifica que desactivar un usuario ya inactivo no falla."""
        user = user_factory(is_active=False)  # Already deactivated
        admin = user_factory(is_staff=True)
        admin.has_perm = Mock(return_value=True)
        
        # Should not raise error
        result = UserService.deactivate_user(
            user=user,
            deactivated_by=admin,
            reason="Segunda desactivación"
        )
        
        assert result.is_active is False
        # Audit log should still be created
        assert AuditLog.objects.filter(
            action=AuditLog.Action.USER_DEACTIVATED,
            resource_id=user.id
        ).exists()

    def test_create_user_manually_success(self, user_factory):
        """Verifica la creación manual de usuarios."""
        admin = user_factory(is_staff=True)
        # Mock permissions
        admin.has_perm = Mock(return_value=True)
        
        # Ensure roles exist
        RoleFactory(code="employee")
        RoleFactory(code="manager")
        
        dob = timezone.now().date().replace(year=2000)
        
        user = UserService.create_user_manually(
            email="newuser@10code.es",
            first_name="New",
            last_name="User",
            date_of_birth=dob,
            roles=["employee", "manager"],
            created_by=admin
        )
        
        assert user.email == "newuser@10code.es"
        assert user.is_active is False
        assert user.has_role("employee")
        assert user.has_role("manager")
        assert user.date_of_birth == dob
        
        assert AuditLog.objects.filter(
            action=AuditLog.Action.USER_CREATED,
            resource_id=user.id
        ).exists()
        
        # Verify role assignment logs
        assert AuditLog.objects.filter(
            action=AuditLog.Action.ROLE_ASSIGNED,
            resource_id=user.id
        ).count() == 2

    def test_create_user_manually_invalid_domain(self, user_factory):
        """Verifica validación de dominio al crear usuario."""
        admin = user_factory(is_staff=True)
        admin.has_perm = Mock(return_value=True)
        
        from django.core.exceptions import ValidationError
        
        with pytest.raises(ValidationError, match="dominio"):
            UserService.create_user_manually(
                email="bad@gmail.com",
                first_name="Bad",
                last_name="Email",
                date_of_birth=timezone.now().date().replace(year=2000),
                roles=[],
                created_by=admin
            )

    def test_create_user_manually_duplicate_email(self, user_factory):
        """Verifica validación de email duplicado."""
        existing = user_factory(email="existing@10code.es")
        admin = user_factory(is_staff=True)
        admin.has_perm = Mock(return_value=True)
        
        from django.core.exceptions import ValidationError
        
        with pytest.raises(ValidationError, match="Ya existe"):
            UserService.create_user_manually(
                email="existing@10code.es",
                first_name="Dup",
                last_name="Email",
                date_of_birth=timezone.now().date().replace(year=2000),
                roles=[],
                created_by=admin
            )

    def test_create_user_manually_underage(self, user_factory):
        """Verifica validación de edad mínima."""
        admin = user_factory(is_staff=True)
        admin.has_perm = Mock(return_value=True)
        
        from django.core.exceptions import ValidationError
        
        # 15 years old
        dob = timezone.now().date().replace(year=timezone.now().year - 15)
        
        with pytest.raises(ValidationError, match="16 años"):
            UserService.create_user_manually(
                email="kid@10code.es",
                first_name="Kid",
                last_name="User",
                date_of_birth=dob,
                roles=[],
                created_by=admin
            )

    def test_create_user_manually_no_permission(self, user_factory):
        """Verifica control de permisos para crear usuarios."""
        admin = user_factory(is_staff=False)
        # Mock permissions to False
        admin.has_perm = Mock(return_value=False)
        
        from django.core.exceptions import PermissionDenied
        
        with pytest.raises(PermissionDenied):
            UserService.create_user_manually(
                email="valid@10code.es",
                first_name="Valid",
                last_name="User",
                date_of_birth=timezone.now().date().replace(year=2000),
                roles=[],
                created_by=admin
            )


@pytest.mark.integration
@pytest.mark.django_db
class TestRoleService:
    """Tests para el servicio de roles."""

    def test_assign_role_to_user(self, user_factory):
        """Verifica la asignación de roles."""
        user = user_factory()
        admin = user_factory(is_staff=True)
        role = RoleFactory(code="test_role")
        
        RoleService.assign_role_to_user(user=user, role_code="test_role", assigned_by=admin)
        
        assert user.has_role("test_role")
        assert AuditLog.objects.filter(
            action=AuditLog.Action.ROLE_ASSIGNED,
            user=admin,
            resource_id=user.id
        ).exists()

