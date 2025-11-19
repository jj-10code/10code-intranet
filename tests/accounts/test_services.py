import pytest
from unittest.mock import Mock
from django.utils import timezone
from apps.accounts.services import AuthService
from apps.accounts.models import AuditLog, Role, UserRole
from tests.factories import UserFactory, RoleFactory

@pytest.mark.django_db
class TestAuthService:
    def test_handle_successful_google_login_first_time(self):
        user = UserFactory(last_login=None)
        request = Mock()
        request.META = {"REMOTE_ADDR": "127.0.0.1"}
        
        # Ensure employee role exists
        RoleFactory(code="employee")

        AuthService.handle_successful_google_login(request=request, user=user)

        user.refresh_from_db()
        assert user.last_login is not None
        assert user.has_role("employee")
        assert AuditLog.objects.filter(user=user, action=AuditLog.Action.LOGIN).exists()

    def test_handle_successful_google_login_returning_user(self):
        user = UserFactory(last_login=timezone.now(), date_joined=timezone.now() - timezone.timedelta(days=1))
        request = Mock()
        request.META = {"REMOTE_ADDR": "127.0.0.1"}
        
        # Ensure employee role exists
        RoleFactory(code="employee")

        AuthService.handle_successful_google_login(request=request, user=user)

        assert not UserRole.objects.filter(user=user, role__code="employee").exists()
        assert AuditLog.objects.filter(user=user, action=AuditLog.Action.LOGIN).exists()

    def test_logout_user(self):
        user = UserFactory()
        request = Mock()
        request.META = {"REMOTE_ADDR": "127.0.0.1"}
        request.session = Mock()

        AuthService.logout_user(request=request, user=user)

        assert AuditLog.objects.filter(user=user, action=AuditLog.Action.LOGOUT).exists()

    def test_log_failed_login(self):
        request = Mock()
        request.META = {"REMOTE_ADDR": "127.0.0.1"}

        AuthService.log_failed_login(request=request, email="fail@example.com")

        assert AuditLog.objects.filter(action=AuditLog.Action.LOGIN_FAILED).exists()
