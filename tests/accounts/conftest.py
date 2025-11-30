"""
Fixtures específicas para el módulo accounts.

Proporciona fixtures reutilizables para testing de autenticación,
roles, permisos y usuarios.
"""

import pytest
from django.test import RequestFactory

from tests.factories import (
    GoogleProfileFactory,
    PermissionFactory,
    RoleFactory,
    UserFactory,
    UserRoleFactory,
)


# ========================================
# Factory Fixtures
# ========================================


@pytest.fixture
def user_factory():
    """Proporciona acceso a UserFactory para crear usuarios en tests."""
    return UserFactory


@pytest.fixture
def role_factory():
    """Proporciona acceso a RoleFactory para crear roles en tests."""
    return RoleFactory


@pytest.fixture
def user_role_factory():
    """Proporciona acceso a UserRoleFactory para asignar roles en tests."""
    return UserRoleFactory


@pytest.fixture
def permission_factory():
    """Proporciona acceso a PermissionFactory para crear permisos en tests."""
    return PermissionFactory


@pytest.fixture
def google_profile_factory():
    """Proporciona acceso a GoogleProfileFactory para crear perfiles OAuth."""
    return GoogleProfileFactory


# ========================================
# Model Instance Fixtures
# ========================================


@pytest.fixture
def user(db):
    """
    Crea un usuario estándar activo.

    Returns:
        User: Usuario regular sin permisos especiales
    """
    return UserFactory()


@pytest.fixture
def admin_user(db):
    """
    Crea un usuario administrador con permisos de staff y superusuario.

    Returns:
        User: Usuario con is_staff=True e is_superuser=True
    """
    return UserFactory(
        email="admin@10code.es",
        first_name="Admin",
        last_name="User",
        is_staff=True,
        is_superuser=True,
        is_active=True,
    )


@pytest.fixture
def inactive_user(db):
    """
    Crea un usuario inactivo.

    Returns:
        User: Usuario con is_active=False
    """
    return UserFactory(is_active=False)


@pytest.fixture
def employee_role(db):
    """
    Crea un rol básico de empleado.

    Returns:
        Role: Rol 'employee' del sistema
    """
    return RoleFactory(
        code="employee",
        name="Employee",
        description="Empleado estándar de 10Code",
        is_system=True,
    )


@pytest.fixture
def manager_role(db):
    """
    Crea un rol de manager.

    Returns:
        Role: Rol 'manager' del sistema
    """
    return RoleFactory(
        code="manager",
        name="Manager",
        description="Manager de equipo",
        is_system=True,
    )


@pytest.fixture
def admin_role(db):
    """
    Crea un rol de administrador.

    Returns:
        Role: Rol 'admin' del sistema
    """
    return RoleFactory(
        code="admin",
        name="Administrator",
        description="Administrador del sistema",
        is_system=True,
    )


@pytest.fixture
def user_with_role(db, user, employee_role):
    """
    Crea un usuario con rol de empleado asignado.

    Returns:
        User: Usuario con rol 'employee' asignado
    """
    UserRoleFactory(user=user, role=employee_role, assigned_by=user)
    return user


# ========================================
# Utility Fixtures
# ========================================


@pytest.fixture
def request_factory():
    """
    Proporciona RequestFactory de Django para crear requests HTTP de prueba.

    Returns:
        RequestFactory: Factory para crear objetos Request
    """
    return RequestFactory()


@pytest.fixture
def authenticated_request(request_factory, user):
    """
    Crea un request HTTP con un usuario autenticado.

    Returns:
        HttpRequest: Request con user autenticado adjunto
    """
    request = request_factory.get("/")
    request.user = user
    return request


@pytest.fixture
def admin_request(request_factory, admin_user):
    """
    Crea un request HTTP con un usuario administrador autenticado.

    Returns:
        HttpRequest: Request con admin_user adjunto
    """
    request = request_factory.get("/")
    request.user = admin_user
    return request


# ========================================
# Cache Override (Autouse)
# ========================================


@pytest.fixture(autouse=True)
def mock_redis_cache(settings):
    """
    Override cache settings to use LocMemCache for all tests.
    This avoids connecting to a real Redis instance.

    Se ejecuta automáticamente para todos los tests.
    """
    settings.CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "unique-snowflake",
        }
    }
    settings.SESSION_ENGINE = "django.contrib.sessions.backends.cache"

