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
        assert AuditLog.objects.filter(action=AuditLog.Action.LOGIN_FAILED).exists()

    @pytest.mark.parametrize("email,expected", [
        ("user@10code.es", True),
        ("admin@10code.es", True),
        ("user@gmail.com", False),
        ("user@other.com", False),
        ("invalid-email", False),
        ("", False),
    ])
    def test_validate_email_domain(self, email, expected):
        assert AuthService.validate_email_domain(email) == expected

@pytest.mark.django_db
class TestUserService:
    def test_update_user_profile(self, user_factory):
        user = user_factory()
        
        from apps.accounts.services import UserService
        UserService.update_user_profile(
            user=user,
            first_name="NewName",
            last_name="NewLast",
            avatar_url="http://new.url/avatar.jpg"
        )
        
        user.refresh_from_db()
        assert user.first_name == "NewName"
        assert user.last_name == "NewLast"
        assert user.avatar_url == "http://new.url/avatar.jpg"

    def test_deactivate_user(self, user_factory):
        user = user_factory(is_active=True)
        admin = user_factory(is_staff=True)
        
        from apps.accounts.services import UserService
        UserService.deactivate_user(user=user, deactivated_by=admin)
        
        user.refresh_from_db()
        assert user.is_active is False
        assert AuditLog.objects.filter(
            action=AuditLog.Action.USER_DEACTIVATED,
            resource_id=user.id
        ).exists()
