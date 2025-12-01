"""
Tests para las vistas del módulo accounts.

Verifica flujos de autenticación, dashboard y gestión de usuarios.
"""

from unittest.mock import Mock

import pytest

from django.urls import reverse

from apps.accounts.models import AuditLog, User
from tests.factories import (
    GoogleProfileFactory,
    RoleFactory,
    UserFactory,
)


@pytest.mark.integration
@pytest.mark.django_db
class TestViews:
    """Tests para vistas generales de autenticación y dashboard."""

    def test_login_view_unauthenticated(self, client):
        """Verifica que la vista de login carga correctamente para usuarios anónimos."""
        url = reverse("login")
        response = client.get(url, **{'HTTP_X_INERTIA': 'true', 'HTTP_X_INERTIA_VERSION': '1.0'})
        assert response.status_code == 200
        data = response.json()
        assert data["component"] == "auth/Login"
        assert "google_login_url" in data["props"]

    def test_login_view_authenticated(self, client, user):
        """Verifica que usuarios autenticados son redirigidos al dashboard."""
        client.force_login(user)
        url = reverse("login")
        response = client.get(url)
        assert response.status_code == 302
        assert response.url == reverse("dashboard")

    def test_dashboard_view(self, client, user):
        """Verifica que el dashboard carga correctamente."""
        client.force_login(user)
        url = reverse("dashboard")
        response = client.get(url, **{'HTTP_X_INERTIA': 'true', 'HTTP_X_INERTIA_VERSION': '1.0'})
        assert response.status_code == 200
        data = response.json()
        assert data["component"] == "Dashboard"
        assert data["props"]["user"]["email"] == user.email

    def test_profile_view(self, client, user):
        """Verifica que el perfil carga correctamente."""
        GoogleProfileFactory(user=user)
        client.force_login(user)
        url = reverse("profile")
        response = client.get(url, **{'HTTP_X_INERTIA': 'true', 'HTTP_X_INERTIA_VERSION': '1.0'})
        assert response.status_code == 200
        data = response.json()
        assert data["component"] == "Profile/Show"
        assert data["props"]["user"]["email"] == user.email

    def test_users_create_get(self, client, admin_user):
        """Verifica que la vista de creación de usuarios carga con permisos."""
        # Asignar permiso específico
        from django.contrib.auth.models import Permission
        from django.contrib.contenttypes.models import ContentType

        content_type = ContentType.objects.get_for_model(User)
        permission = Permission.objects.get(codename="add_user", content_type=content_type)
        admin_user.user_permissions.add(permission)

        client.force_login(admin_user)

        RoleFactory(code="employee", name="Employee")

        url = reverse("users_create")
        response = client.get(url, **{'HTTP_X_INERTIA': 'true', 'HTTP_X_INERTIA_VERSION': '1.0'})

        assert response.status_code == 200
        data = response.json()
        assert data["component"] == "Users/Create"
        assert len(data["props"]["available_roles"]) >= 1
        assert data["props"]["permissions"]["can_assign_roles"] is True

    def test_users_create_post_success(self, client, admin_user):
        """Verifica la creación exitosa de un usuario vía POST."""
        # Asignar permiso
        from django.contrib.auth.models import Permission
        from django.contrib.contenttypes.models import ContentType

        content_type = ContentType.objects.get_for_model(User)
        permission = Permission.objects.get(codename="add_user", content_type=content_type)
        admin_user.user_permissions.add(permission)

        client.force_login(admin_user)

        RoleFactory(code="employee")

        url = reverse("users_create")
        from django.utils import timezone
        dob = timezone.now().date().replace(year=2000)

        data = {
            "email": "newuser@10code.es",
            "first_name": "New",
            "last_name": "User",
            "date_of_birth": dob.isoformat(),
            "roles": ["employee"],
        }

        response = client.post(url, data)

        assert response.status_code == 302
        assert response.url == reverse("users_index")

        assert User.objects.filter(email="newuser@10code.es").exists()

    def test_users_create_permission(self, client, user):
        """Verifica que se deniega acceso sin permisos."""
        # Mock permissions to False
        user.has_perm = Mock(return_value=False)
        client.force_login(user)

        url = reverse("users_create")
        response = client.get(url)

        # permission_required raises PermissionDenied which Django handles as 403
        assert response.status_code == 403

    def test_users_index_view(self, client, admin_user):
        """Verifica que la vista de listado de usuarios carga correctamente."""
        # Asignar permiso view_user
        from django.contrib.auth.models import Permission
        from django.contrib.contenttypes.models import ContentType

        content_type = ContentType.objects.get_for_model(User)
        permission = Permission.objects.get(codename="view_user", content_type=content_type)
        admin_user.user_permissions.add(permission)

        # Crear algunos usuarios de prueba
        UserFactory.create_batch(5)

        client.force_login(admin_user)
        url = reverse("users_index")
        response = client.get(url, **{'HTTP_X_INERTIA': 'true', 'HTTP_X_INERTIA_VERSION': '1.0'})

        assert response.status_code == 200
        data = response.json()
        assert data["component"] == "Users/Index"
        assert "users" in data["props"]
        assert "filters" in data["props"]
        assert "pagination" in data["props"]
        assert "permissions" in data["props"]

        # Verificar estructura de paginación
        pagination = data["props"]["pagination"]
        assert "current_page" in pagination
        assert "total_pages" in pagination
        assert "has_next" in pagination
        assert "has_previous" in pagination

        # Verificar permisos
        permissions = data["props"]["permissions"]
        assert "can_create" in permissions

    def test_users_index_pagination(self, client, admin_user):
        """Verifica que la paginación funciona correctamente."""
        # Asignar permiso
        from django.contrib.auth.models import Permission
        from django.contrib.contenttypes.models import ContentType

        content_type = ContentType.objects.get_for_model(User)
        permission = Permission.objects.get(codename="view_user", content_type=content_type)
        admin_user.user_permissions.add(permission)

        # Crear más usuarios que el límite de página (20)
        UserFactory.create_batch(25)

        client.force_login(admin_user)
        url = reverse("users_index")

        # Página 1
        response = client.get(url, **{'HTTP_X_INERTIA': 'true', 'HTTP_X_INERTIA_VERSION': '1.0'})
        data = response.json()
        assert len(data["props"]["users"]) == 20
        assert data["props"]["pagination"]["current_page"] == 1
        assert data["props"]["pagination"]["has_next"] is True
        assert data["props"]["pagination"]["has_previous"] is False

        # Página 2
        response = client.get(f"{url}?page=2", **{'HTTP_X_INERTIA': 'true', 'HTTP_X_INERTIA_VERSION': '1.0'})
        data = response.json()
        assert len(data["props"]["users"]) == 6  # 25 total - 20 en página 1 = 5, pero +1 admin_user = 6
        assert data["props"]["pagination"]["current_page"] == 2
        assert data["props"]["pagination"]["has_next"] is False
        assert data["props"]["pagination"]["has_previous"] is True

    def test_users_index_filters(self, client, admin_user, role_factory, user_role_factory):
        """Verifica que los filtros se aplican correctamente."""
        # Asignar permiso
        from django.contrib.auth.models import Permission
        from django.contrib.contenttypes.models import ContentType

        content_type = ContentType.objects.get_for_model(User)
        permission = Permission.objects.get(codename="view_user", content_type=content_type)
        admin_user.user_permissions.add(permission)

        # Crear usuarios con diferentes estados y roles
        active_user = UserFactory(is_active=True, email="active@10code.es")
        UserFactory(is_active=False, email="inactive@10code.es")  # Usuario inactivo
        admin_role = role_factory(code="admin")
        employee_role = role_factory(code="employee")

        user_role_factory(user=active_user, role=admin_role)
        user_with_employee_role = UserFactory(is_active=True, email="employee@10code.es")
        user_role_factory(user=user_with_employee_role, role=employee_role)

        client.force_login(admin_user)
        url = reverse("users_index")

        # Filtrar por activos
        response = client.get(f"{url}?is_active=true", **{'HTTP_X_INERTIA': 'true', 'HTTP_X_INERTIA_VERSION': '1.0'})
        data = response.json()
        # Debería incluir active_user, user_with_employee_role, y admin_user
        assert len(data["props"]["users"]) >= 3
        active_emails = [u["email"] for u in data["props"]["users"]]
        assert active_user.email in active_emails
        assert user_with_employee_role.email in active_emails

        # Filtrar por rol
        response = client.get(f"{url}?role=admin", **{'HTTP_X_INERTIA': 'true', 'HTTP_X_INERTIA_VERSION': '1.0'})
        data = response.json()
        assert len(data["props"]["users"]) >= 1
        admin_user_emails = [u["email"] for u in data["props"]["users"]]
        assert active_user.email in admin_user_emails

        # Filtrar por búsqueda
        response = client.get(f"{url}?search=active", **{'HTTP_X_INERTIA': 'true', 'HTTP_X_INERTIA_VERSION': '1.0'})
        data = response.json()
        assert len(data["props"]["users"]) >= 1
        search_results = [u["email"] for u in data["props"]["users"]]
        assert active_user.email in search_results

    def test_users_index_permission_required(self, client, user):
        """Verifica que se requiere permiso view_user."""
        client.force_login(user)
        url = reverse("users_index")
        response = client.get(url)

        # permission_required raises PermissionDenied which Django handles as 403
        assert response.status_code == 403


@pytest.mark.integration
@pytest.mark.django_db
class TestUsersDeactivateView:
    """Tests para la vista de desactivación de usuarios."""

    def test_deactivate_user_success(self, client, admin_user):
        """Test successful user deactivation with permission."""
        user_to_deactivate = UserFactory(is_active=True, email="deactivate@10code.es")

        # Grant permission
        from django.contrib.auth.models import Permission
        from django.contrib.contenttypes.models import ContentType

        content_type = ContentType.objects.get_for_model(User)
        permission = Permission.objects.get(codename="delete_user", content_type=content_type)
        admin_user.user_permissions.add(permission)

        client.force_login(admin_user)

        url = reverse("users_deactivate", kwargs={"user_id": user_to_deactivate.id})
        response = client.post(url, {"reason": "Baja temporal por excedencia"})

        assert response.status_code == 302
        assert response.url == reverse("users_index")

        # Verify user was deactivated
        user_to_deactivate.refresh_from_db()
        assert user_to_deactivate.is_active is False

        # Verify audit log
        assert AuditLog.objects.filter(
            action=AuditLog.Action.USER_DEACTIVATED,
            resource_id=user_to_deactivate.id
        ).exists()

    def test_deactivate_user_without_permission(self, client, user):
        """Test deactivation fails without permission."""
        user_to_deactivate = UserFactory(is_active=True)

        client.force_login(user)

        url = reverse("users_deactivate", kwargs={"user_id": user_to_deactivate.id})
        response = client.post(url, {"reason": "Intentando desactivar"})

        # Should redirect with error message (flash message logic)
        assert response.status_code == 302
        assert response.url == reverse("users_index")

        # User should still be active
        user_to_deactivate.refresh_from_db()
        assert user_to_deactivate.is_active is True

    def test_deactivate_user_missing_reason(self, client, admin_user):
        """Test deactivation fails without reason."""
        user_to_deactivate = UserFactory(is_active=True)

        from django.contrib.auth.models import Permission
        from django.contrib.contenttypes.models import ContentType

        content_type = ContentType.objects.get_for_model(User)
        permission = Permission.objects.get(codename="delete_user", content_type=content_type)
        admin_user.user_permissions.add(permission)

        client.force_login(admin_user)

        url = reverse("users_deactivate", kwargs={"user_id": user_to_deactivate.id})
        # POST without reason
        response = client.post(url, {})

        assert response.status_code == 302
        assert response.url == reverse("users_index")

        # User should still be active
        user_to_deactivate.refresh_from_db()
        assert user_to_deactivate.is_active is True

    def test_deactivate_user_not_found(self, client, admin_user):
        """Test deactivation with non-existent user ID."""
        from django.contrib.auth.models import Permission
        from django.contrib.contenttypes.models import ContentType

        content_type = ContentType.objects.get_for_model(User)
        permission = Permission.objects.get(codename="delete_user", content_type=content_type)
        admin_user.user_permissions.add(permission)

        client.force_login(admin_user)

        # Use non-existent user ID
        url = reverse("users_deactivate", kwargs={"user_id": 99999})
        response = client.post(url, {"reason": "Testing 404"})

        # Should return 404
        assert response.status_code == 404


