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

