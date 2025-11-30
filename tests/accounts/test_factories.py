"""
Tests para verificar que las factories funcionan correctamente.

Verifica la creación de objetos de prueba usando las factories definidas.
"""

import pytest

from apps.accounts.models import Permission, Role, User, UserRole
from tests.factories import (
    PermissionFactory,
    RoleFactory,
    UserFactory,
    UserRoleFactory,
)


@pytest.mark.unit
class TestUserFactory:
    """Tests para UserFactory."""

    def test_create_user(self, db):
        """Verifica que UserFactory crea un usuario válido."""
        user = UserFactory()

        assert isinstance(user, User)
        assert user.email
        assert user.first_name
        assert user.last_name
        assert user.is_active is True
        assert "@10code.es" in user.email

    def test_create_multiple_users(self, db):
        """Verifica que se pueden crear múltiples usuarios con emails únicos."""
        user1 = UserFactory()
        user2 = UserFactory()

        assert user1.email != user2.email
        assert User.objects.count() == 2

    def test_create_admin_user(self, db):
        """Verifica la creación de un usuario administrador."""
        admin = UserFactory(is_staff=True, is_superuser=True)

        assert admin.is_staff is True
        assert admin.is_superuser is True


@pytest.mark.unit
class TestRoleFactory:
    """Tests para RoleFactory."""

    def test_create_role(self, db):
        """Verifica que RoleFactory crea un rol válido."""
        role = RoleFactory()

        assert isinstance(role, Role)
        assert role.code
        assert role.name
        assert role.is_system is False

    def test_create_system_role(self, db):
        """Verifica la creación de un rol del sistema."""
        role = RoleFactory(code="admin", name="Administrator", is_system=True)

        assert role.code == "admin"
        assert role.is_system is True


@pytest.mark.unit
class TestUserRoleFactory:
    """Tests para UserRoleFactory."""

    def test_create_user_role(self, db):
        """Verifica que UserRoleFactory crea una asignación de rol válida."""
        user_role = UserRoleFactory()

        assert isinstance(user_role, UserRole)
        assert user_role.user
        assert user_role.role
        assert user_role.assigned_by
        assert user_role.assigned_at

    def test_assign_role_to_existing_user(self, db):
        """Verifica la asignación de un rol a un usuario existente."""
        user = UserFactory()
        role = RoleFactory(code="employee", name="Employee")
        admin = UserFactory(is_staff=True)

        user_role = UserRoleFactory(user=user, role=role, assigned_by=admin)

        assert user_role.user == user
        assert user_role.role == role
        assert user_role.assigned_by == admin

    def test_user_has_role_method(self, db):
        """Verifica que el método has_role funciona correctamente."""
        user = UserFactory()
        role = RoleFactory(code="manager", name="Manager")
        UserRoleFactory(user=user, role=role)

        assert user.has_role("manager") is True
        assert user.has_role("admin") is False


@pytest.mark.unit
class TestPermissionFactory:
    """Tests para PermissionFactory."""

    def test_create_permission(self, db):
        """Verifica que PermissionFactory crea un permiso válido."""
        permission = PermissionFactory()

        assert isinstance(permission, Permission)
        assert permission.role
        assert permission.permission_code
        assert "." in permission.permission_code  # Debe tener formato app.action_model

    def test_create_permission_for_role(self, db):
        """Verifica la creación de permisos específicos para un rol."""
        role = RoleFactory(code="manager")
        permission = PermissionFactory(
            role=role, permission_code="projects.add_project"
        )

        assert permission.role == role
        assert permission.permission_code == "projects.add_project"


@pytest.mark.unit
class TestFixtures:
    """Tests para verificar que las fixtures funcionan correctamente."""

    def test_user_fixture(self, user):
        """Verifica que la fixture 'user' funciona."""
        assert isinstance(user, User)
        assert user.is_active is True

    def test_admin_user_fixture(self, admin_user):
        """Verifica que la fixture 'admin_user' funciona."""
        assert isinstance(admin_user, User)
        assert admin_user.is_staff is True
        assert admin_user.is_superuser is True
        assert admin_user.email == "admin@10code.es"

    def test_employee_role_fixture(self, employee_role):
        """Verifica que la fixture 'employee_role' funciona."""
        assert isinstance(employee_role, Role)
        assert employee_role.code == "employee"
        assert employee_role.is_system is True

    def test_manager_role_fixture(self, manager_role):
        """Verifica que la fixture 'manager_role' funciona."""
        assert isinstance(manager_role, Role)
        assert manager_role.code == "manager"

    def test_admin_role_fixture(self, admin_role):
        """Verifica que la fixture 'admin_role' funciona."""
        assert isinstance(admin_role, Role)
        assert admin_role.code == "admin"

    def test_user_with_role_fixture(self, user_with_role):
        """Verifica que la fixture 'user_with_role' funciona."""
        assert isinstance(user_with_role, User)
        assert user_with_role.has_role("employee") is True

    def test_authenticated_request_fixture(self, authenticated_request):
        """Verifica que la fixture 'authenticated_request' funciona."""
        assert authenticated_request.user
        assert authenticated_request.user.is_authenticated

    def test_admin_request_fixture(self, admin_request):
        """Verifica que la fixture 'admin_request' funciona."""
        assert admin_request.user
        assert admin_request.user.is_staff is True
