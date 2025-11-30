"""
Configuración global de pytest para el proyecto.

Proporciona fixtures base disponibles para todos los módulos de tests.
"""

import pytest
from rest_framework.test import APIClient

from tests.factories import UserFactory


@pytest.fixture
def api_client():
    """
    Proporciona un cliente de API de Django REST Framework.

    Returns:
        APIClient: Cliente sin autenticación
    """
    return APIClient()


@pytest.fixture
def user(db):
    """
    Crea un usuario estándar para tests.

    Returns:
        User: Usuario regular activo
    """
    return UserFactory()


@pytest.fixture
def admin_user(db):
    """
    Crea un usuario administrador para tests.

    Returns:
        User: Usuario con permisos de administrador
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
def authenticated_client(api_client, user):
    """
    Proporciona un cliente de API autenticado con un usuario regular.

    Returns:
        APIClient: Cliente autenticado como user
    """
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def admin_client(api_client, admin_user):
    """
    Proporciona un cliente de API autenticado con un usuario administrador.

    Returns:
        APIClient: Cliente autenticado como admin_user
    """
    api_client.force_authenticate(user=admin_user)
    return api_client

