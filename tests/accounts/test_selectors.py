"""
Tests para los selectors del módulo accounts.

Verifica funciones de consulta de usuarios, roles y permisos.
"""

import pytest

from apps.accounts.selectors import (
    get_active_users,
    get_user_by_email,
    get_user_by_id,
    user_has_any_role,
    user_has_role,
)
from tests.factories import UserRoleFactory


@pytest.mark.unit
@pytest.mark.django_db
class TestSelectors:
    """Tests para los selectors de usuarios y roles."""

    def test_get_user_by_email(self, user_factory):
        """Verifica que get_user_by_email encuentra usuarios activos."""
        user = user_factory(email="test@10code.es")
        found_user = get_user_by_email(email="test@10code.es")
        assert found_user == user

    def test_get_user_by_email_not_found(self):
        """Verifica que retorna None cuando el email no existe."""
        found_user = get_user_by_email(email="nonexistent@10code.es")
        assert found_user is None

    def test_get_user_by_email_inactive(self, user_factory):
        """Verifica que usuarios inactivos no son retornados."""
        user_factory(email="inactive@10code.es", is_active=False)
        found_user = get_user_by_email(email="inactive@10code.es")
        assert found_user is None

    def test_get_user_by_id(self, user_factory):
        """Verifica que get_user_by_id encuentra usuarios activos por ID."""
        user = user_factory()
        found_user = get_user_by_id(user_id=user.id)
        assert found_user == user

    def test_get_user_by_id_not_found(self):
        """Verifica que retorna None cuando el ID no existe."""
        found_user = get_user_by_id(user_id=999)
        assert found_user is None

    def test_get_user_by_id_inactive(self, user_factory):
        """Verifica que usuarios inactivos no son retornados por ID."""
        user = user_factory(is_active=False)
        found_user = get_user_by_id(user_id=user.id)
        assert found_user is None

    def test_get_active_users(self, user_factory):
        """Verifica que get_active_users solo retorna usuarios activos."""
        user1 = user_factory(email="a@10code.es", is_active=True)
        user2 = user_factory(email="b@10code.es", is_active=True)
        user_factory(email="c@10code.es", is_active=False)

        active_users = get_active_users()
        assert active_users.count() == 2
        assert user1 in active_users
        assert user2 in active_users

    def test_user_has_role(self, user_factory, role_factory):
        """Verifica que user_has_role detecta correctamente roles asignados."""
        user = user_factory()
        role = role_factory(code="admin")
        UserRoleFactory(user=user, role=role)

        assert user_has_role(user=user, role_code="admin") is True
        assert user_has_role(user=user, role_code="employee") is False

    def test_user_has_any_role(self, user_factory, role_factory):
        """Verifica que user_has_any_role detecta múltiples roles correctamente."""
        user = user_factory()
        role1 = role_factory(code="admin")
        role_factory(code="manager")
        UserRoleFactory(user=user, role=role1)

        assert user_has_any_role(user=user, role_codes=["admin", "employee"]) is True
        assert user_has_any_role(user=user, role_codes=["manager", "employee"]) is False
        assert user_has_any_role(user=user, role_codes=["employee"]) is False
