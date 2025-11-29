import pytest
from django.urls import reverse
from tests.factories import UserFactory, GoogleProfileFactory, RoleFactory

@pytest.mark.django_db
class TestViews:
    def test_login_view_unauthenticated(self, client):
        url = reverse("login")
        response = client.get(url, **{'HTTP_X_INERTIA': 'true', 'HTTP_X_INERTIA_VERSION': '1.0'})
        assert response.status_code == 200
        data = response.json()
        assert data["component"] == "auth/Login"
        assert "google_login_url" in data["props"]

    def test_login_view_authenticated(self, client):
        user = UserFactory()
        client.force_login(user)
        url = reverse("login")
        response = client.get(url)
        assert response.status_code == 302
        assert response.url == reverse("dashboard")

    def test_dashboard_view(self, client):
        user = UserFactory()
        client.force_login(user)
        url = reverse("dashboard")
        response = client.get(url, **{'HTTP_X_INERTIA': 'true', 'HTTP_X_INERTIA_VERSION': '1.0'})
        assert response.status_code == 200
        data = response.json()
        assert data["component"] == "Dashboard"
        assert data["props"]["user"]["email"] == user.email

    def test_profile_view(self, client):
        user = UserFactory()
        GoogleProfileFactory(user=user)
        client.force_login(user)
        url = reverse("profile")
        response = client.get(url, **{'HTTP_X_INERTIA': 'true', 'HTTP_X_INERTIA_VERSION': '1.0'})
        assert response.status_code == 200
        data = response.json()
        assert data["component"] == "profile/Show"
        assert data["props"]["user"]["email"] == user.email

    def test_users_create_get(self, client):
        user = UserFactory(is_staff=True)
        # Assign permission
        from django.contrib.auth.models import Permission
        from django.contrib.contenttypes.models import ContentType
        from apps.accounts.models import User
        
        content_type = ContentType.objects.get_for_model(User)
        permission = Permission.objects.get(codename="add_user", content_type=content_type)
        user.user_permissions.add(permission)
        
        client.force_login(user)
        
        RoleFactory(code="employee", name="Employee")
        
        url = reverse("users_create")
        response = client.get(url, **{'HTTP_X_INERTIA': 'true', 'HTTP_X_INERTIA_VERSION': '1.0'})
        
        assert response.status_code == 200
        data = response.json()
        assert data["component"] == "Users/Create"
        assert len(data["props"]["available_roles"]) >= 1
        assert data["props"]["permissions"]["can_assign_roles"] is True

    def test_users_create_post_success(self, client):
        user = UserFactory(is_staff=True)
        from django.contrib.auth.models import Permission
        from django.contrib.contenttypes.models import ContentType
        from apps.accounts.models import User
        
        content_type = ContentType.objects.get_for_model(User)
        permission = Permission.objects.get(codename="add_user", content_type=content_type)
        user.user_permissions.add(permission)
        
        client.force_login(user)
        
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

    def test_users_create_permission(self, client):
        user = UserFactory(is_staff=False)
        # Mock permissions to False
        from unittest.mock import Mock
        user.has_perm = Mock(return_value=False)
        client.force_login(user)
        
        url = reverse("users_create")
        response = client.get(url)
        
        # permission_required raises PermissionDenied which Django handles as 403
        assert response.status_code == 403


@pytest.mark.django_db
class TestUsersDeactivateView:
    def test_deactivate_user_success(self, client):
        """Test successful user deactivation with permission."""
        admin = UserFactory(is_staff=True)
        user_to_deactivate = UserFactory(is_active=True, email="deactivate@10code.es")
        
        # Grant permission
        from django.contrib.auth.models import Permission
        from django.contrib.contenttypes.models import ContentType
        from apps.accounts.models import User
        
        content_type = ContentType.objects.get_for_model(User)
        permission = Permission.objects.get(codename="delete_user", content_type=content_type)
        admin.user_permissions.add(permission)
        
        client.force_login(admin)
        
        url = reverse("users_deactivate", kwargs={"user_id": user_to_deactivate.id})
        response = client.post(url, {"reason": "Baja temporal por excedencia"})
        
        assert response.status_code == 302
        assert response.url == reverse("users_index")
        
        # Verify user was deactivated
        user_to_deactivate.refresh_from_db()
        assert user_to_deactivate.is_active is False
        
        # Verify audit log
        from apps.accounts.models import AuditLog
        assert AuditLog.objects.filter(
            action=AuditLog.Action.USER_DEACTIVATED,
            resource_id=user_to_deactivate.id
        ).exists()

    def test_deactivate_user_without_permission(self, client):
        """Test deactivation fails without permission."""
        regular_user = UserFactory(is_staff=False)
        user_to_deactivate = UserFactory(is_active=True)
        
        client.force_login(regular_user)
        
        url = reverse("users_deactivate", kwargs={"user_id": user_to_deactivate.id})
        response = client.post(url, {"reason": "Intentando desactivar"})
        
        # Should redirect with error message
        assert response.status_code == 302
        assert response.url == reverse("users_index")
        
        # User should still be active
        user_to_deactivate.refresh_from_db()
        assert user_to_deactivate.is_active is True

    def test_deactivate_user_missing_reason(self, client):
        """Test deactivation fails without reason."""
        admin = UserFactory(is_staff=True)
        user_to_deactivate = UserFactory(is_active=True)
        
        from django.contrib.auth.models import Permission
        from django.contrib.contenttypes.models import ContentType
        from apps.accounts.models import User
        
        content_type = ContentType.objects.get_for_model(User)
        permission = Permission.objects.get(codename="delete_user", content_type=content_type)
        admin.user_permissions.add(permission)
        
        client.force_login(admin)
        
        url = reverse("users_deactivate", kwargs={"user_id": user_to_deactivate.id})
        # POST without reason
        response = client.post(url, {})
        
        assert response.status_code == 302
        assert response.url == reverse("users_index")
        
        # User should still be active
        user_to_deactivate.refresh_from_db()
        assert user_to_deactivate.is_active is True

    def test_deactivate_user_not_found(self, client):
        """Test deactivation with non-existent user ID."""
        admin = UserFactory(is_staff=True)
        
        from django.contrib.auth.models import Permission
        from django.contrib.contenttypes.models import ContentType
        from apps.accounts.models import User
        
        content_type = ContentType.objects.get_for_model(User)
        permission = Permission.objects.get(codename="delete_user", content_type=content_type)
        admin.user_permissions.add(permission)
        
        client.force_login(admin)
        
        # Use non-existent user ID
        url = reverse("users_deactivate", kwargs={"user_id": 99999})
        response = client.post(url, {"reason": "Testing 404"})
        
        # Should return 404
        assert response.status_code == 404


