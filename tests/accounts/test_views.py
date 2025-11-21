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
        assert data["component"] == "Auth/Login"
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
        assert data["component"] == "Dashboard/Index"
        assert data["props"]["user"]["email"] == user.email

    def test_profile_view(self, client):
        user = UserFactory()
        GoogleProfileFactory(user=user)
        client.force_login(user)
        url = reverse("profile")
        response = client.get(url, **{'HTTP_X_INERTIA': 'true', 'HTTP_X_INERTIA_VERSION': '1.0'})
        assert response.status_code == 200
        data = response.json()
        assert data["component"] == "Profile/Show"
        assert data["props"]["user"]["email"] == user.email

