"""
Tests para los selectors del módulo accounts.

Verifica funciones de consulta de usuarios, roles y permisos.
"""

import pytest

from apps.accounts.selectors import (
    UserSelector,
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

    def test_get_users_list_basic(self, user_factory):
        """Verifica que get_users_list retorna todos los usuarios ordenados por fecha."""
        user1 = user_factory(email="a@10code.es")
        user2 = user_factory(email="b@10code.es")

        qs = UserSelector.get_users_list(user=user1)
        users = list(qs)

        assert len(users) == 2
        # Ordenado por -date_joined, el último creado primero
        assert users[0] == user2
        assert users[1] == user1

    def test_get_users_list_filter_is_active(self, user_factory):
        """Verifica filtro por is_active."""
        active_user = user_factory(email="active@10code.es", is_active=True)
        user_factory(email="inactive@10code.es", is_active=False)  # Create inactive user

        qs = UserSelector.get_users_list(user=active_user, filters={"is_active": True})
        users = list(qs)

        assert len(users) == 1
        assert users[0] == active_user

    def test_get_users_list_filter_role(self, user_factory, role_factory, user_role_factory):
        """Verifica filtro por rol."""
        user1 = user_factory(email="admin@10code.es")
        user2 = user_factory(email="employee@10code.es")
        admin_role = role_factory(code="admin")
        employee_role = role_factory(code="employee")

        user_role_factory(user=user1, role=admin_role)
        user_role_factory(user=user2, role=employee_role)

        qs = UserSelector.get_users_list(user=user1, filters={"role": "admin"})
        users = list(qs)

        assert len(users) == 1
        assert users[0] == user1

    def test_get_users_list_filter_search(self, user_factory):
        """Verifica filtro por búsqueda en email, nombre y apellidos."""
        user1 = user_factory(email="john@10code.es", first_name="John", last_name="Doe")
        user2 = user_factory(email="jane@10code.es", first_name="Jane", last_name="Smith")

        # Buscar por email
        qs = UserSelector.get_users_list(user=user1, filters={"search": "john"})
        users = list(qs)
        assert len(users) == 1
        assert users[0] == user1

        # Buscar por nombre
        qs = UserSelector.get_users_list(user=user1, filters={"search": "Jane"})
        users = list(qs)
        assert len(users) == 1
        assert users[0] == user2

        # Buscar por apellido
        qs = UserSelector.get_users_list(user=user1, filters={"search": "Smith"})
        users = list(qs)
        assert len(users) == 1
        assert users[0] == user2

    def test_get_users_list_combined_filters(self, user_factory, role_factory, user_role_factory):
        """Verifica combinación de filtros."""
        user1 = user_factory(email="admin@10code.es", first_name="Admin", is_active=True)
        user_factory(email="inactive@10code.es", first_name="Inactive", is_active=False)  # Create inactive user
        admin_role = role_factory(code="admin")

        user_role_factory(user=user1, role=admin_role)

        # Filtro por rol y búsqueda
        qs = UserSelector.get_users_list(
            user=user1,
            filters={"role": "admin", "search": "Admin", "is_active": True}
        )
        users = list(qs)

        assert len(users) == 1
        assert users[0] == user1

