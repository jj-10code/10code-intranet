import pytest
from django.urls import reverse
from tests.factories import UserFactory, GoogleProfileFactory, RoleFactory

@pytest.mark.django_db
class TestViews:
    def test_login_view_unauthenticated(self, client):
        url = reverse("login")
        response = client.get(url)
        assert response.status_code == 200
        assert "Auth/Login" in response.context["page_component"]

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
        response = client.get(url)
        assert response.status_code == 200
        assert "Dashboard/Index" in response.context["page_component"]
        props = response.context["page_props"]
        assert props["user"]["email"] == user.email

    def test_profile_view(self, client):
        user = UserFactory()
        GoogleProfileFactory(user=user)
        client.force_login(user)
        url = reverse("profile")
        response = client.get(url)
        assert response.status_code == 200
        assert "Profile/Show" in response.context["page_component"]
        props = response.context["page_props"]
        assert props["user"]["email"] == user.email
