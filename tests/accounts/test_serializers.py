import pytest
from datetime import date
from apps.accounts.serializers import UserSerializer, RoleSerializer
from tests.factories import UserRoleFactory

@pytest.mark.unit
@pytest.mark.django_db
class TestSerializers:
    def test_role_serializer(self, role_factory):
        role = role_factory(
            code="admin",
            name="Administrador",
            description="Rol de admin",
            is_system=True
        )
        data = RoleSerializer(role)
        assert data == {
            "id": role.id,
            "code": "admin",
            "name": "Administrador",
            "description": "Rol de admin",
            "is_system": True,
        }

    def test_user_serializer(self, user_factory, role_factory):
        user = user_factory(
            email="test@example.com",
            first_name="Juan",
            last_name="Perez",
            avatar_url="http://example.com/avatar.jpg",
            is_active=True,
            date_of_birth=date(1990, 1, 1)
        )
        role1 = role_factory(name="Admin")
        role2 = role_factory(name="Editor")
        UserRoleFactory(user=user, role=role1)
        UserRoleFactory(user=user, role=role2)
        
        data = UserSerializer(user)
        
        assert data["id"] == user.id
        assert data["email"] == "test@example.com"
        assert data["first_name"] == "Juan"
        assert data["last_name"] == "Perez"
        assert data["avatar_url"] == "http://example.com/avatar.jpg"
        assert data["is_active"] is True
        assert data["date_of_birth"] == "1990-01-01"
        assert set(data["roles"]) == {"Admin", "Editor"}

    def test_user_serializer_no_dob(self, user_factory):
        user = user_factory(date_of_birth=None)
        data = UserSerializer(user)
        assert data["date_of_birth"] is None
