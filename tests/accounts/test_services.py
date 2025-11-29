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

    def test_create_user_manually_success(self, user_factory):
        admin = user_factory(is_staff=True)
        # Mock permissions
        admin.has_perm = Mock(return_value=True)
        
        # Ensure roles exist
        RoleFactory(code="employee")
        RoleFactory(code="manager")
        
        from apps.accounts.services import UserService
        
        dob = timezone.now().date().replace(year=2000)
        
        user = UserService.create_user_manually(
            email="newuser@10code.es",
            first_name="New",
            last_name="User",
            date_of_birth=dob,
            roles=["employee", "manager"],
            created_by=admin
        )
        
        assert user.email == "newuser@10code.es"
        assert user.is_active is False
        assert user.has_role("employee")
        assert user.has_role("manager")
        assert user.date_of_birth == dob
        
        assert AuditLog.objects.filter(
            action=AuditLog.Action.USER_CREATED,
            resource_id=user.id
        ).exists()
        
        # Verify role assignment logs
        assert AuditLog.objects.filter(
            action=AuditLog.Action.ROLE_ASSIGNED,
            resource_id=user.id
        ).count() == 2

    def test_create_user_manually_invalid_domain(self, user_factory):
        admin = user_factory(is_staff=True)
        admin.has_perm = Mock(return_value=True)
        
        from apps.accounts.services import UserService
        from django.core.exceptions import ValidationError
        
        with pytest.raises(ValidationError, match="dominio"):
            UserService.create_user_manually(
                email="bad@gmail.com",
                first_name="Bad",
                last_name="Email",
                date_of_birth=timezone.now().date().replace(year=2000),
                roles=[],
                created_by=admin
            )

    def test_create_user_manually_duplicate_email(self, user_factory):
        existing = user_factory(email="existing@10code.es")
        admin = user_factory(is_staff=True)
        admin.has_perm = Mock(return_value=True)
        
        from apps.accounts.services import UserService
        from django.core.exceptions import ValidationError
        
        with pytest.raises(ValidationError, match="Ya existe"):
            UserService.create_user_manually(
                email="existing@10code.es",
                first_name="Dup",
                last_name="Email",
                date_of_birth=timezone.now().date().replace(year=2000),
                roles=[],
                created_by=admin
            )

    def test_create_user_manually_underage(self, user_factory):
        admin = user_factory(is_staff=True)
        admin.has_perm = Mock(return_value=True)
        
        from apps.accounts.services import UserService
        from django.core.exceptions import ValidationError
        
        # 15 years old
        dob = timezone.now().date().replace(year=timezone.now().year - 15)
        
        with pytest.raises(ValidationError, match="16 años"):
            UserService.create_user_manually(
                email="kid@10code.es",
                first_name="Kid",
                last_name="User",
                date_of_birth=dob,
                roles=[],
                created_by=admin
            )

    def test_create_user_manually_no_permission(self, user_factory):
        admin = user_factory(is_staff=False)
        # Mock permissions to False
        admin.has_perm = Mock(return_value=False)
        
        from apps.accounts.services import UserService
        from django.core.exceptions import PermissionDenied
        
        with pytest.raises(PermissionDenied):
            UserService.create_user_manually(
                email="valid@10code.es",
                first_name="Valid",
                last_name="User",
                date_of_birth=timezone.now().date().replace(year=2000),
                roles=[],
                created_by=admin
            )

@pytest.mark.django_db
class TestRoleService:
    def test_assign_role_to_user(self, user_factory):
        user = user_factory()
        admin = user_factory(is_staff=True)
        role = RoleFactory(code="test_role")
        
        from apps.accounts.services import RoleService
        
        RoleService.assign_role_to_user(user=user, role_code="test_role", assigned_by=admin)
        
        assert user.has_role("test_role")
        assert AuditLog.objects.filter(
            action=AuditLog.Action.ROLE_ASSIGNED,
            user=admin,
            resource_id=user.id
        ).exists()
