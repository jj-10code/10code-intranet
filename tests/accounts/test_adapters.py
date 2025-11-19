import pytest
from unittest.mock import Mock
from django.core.exceptions import PermissionDenied
from allauth.socialaccount.models import SocialLogin, SocialAccount
from apps.accounts.adapters import SocialAccountAdapter
from apps.accounts.models import GoogleProfile
from tests.factories import UserFactory

@pytest.mark.django_db
class TestSocialAccountAdapter:
    def test_pre_social_login_allowed_domain(self):
        adapter = SocialAccountAdapter()
        request = Mock()
        sociallogin = Mock(spec=SocialLogin)
        sociallogin.account = Mock(spec=SocialAccount)
        sociallogin.account.extra_data = {"email": "test@10code.es", "hd": "10code.es"}

        # Should not raise exception
        adapter.pre_social_login(request, sociallogin)

    def test_pre_social_login_invalid_domain(self):
        adapter = SocialAccountAdapter()
        request = Mock()
        sociallogin = Mock(spec=SocialLogin)
        sociallogin.account = Mock(spec=SocialAccount)
        sociallogin.account.extra_data = {"email": "test@gmail.com"}

        with pytest.raises(PermissionDenied):
            adapter.pre_social_login(request, sociallogin)

    def test_populate_user(self):
        adapter = SocialAccountAdapter()
        request = Mock()
        sociallogin = Mock(spec=SocialLogin)
        sociallogin.account = Mock(spec=SocialAccount)
        sociallogin.account.extra_data = {
            "given_name": "John",
            "family_name": "Doe",
            "picture": "http://example.com/avatar.jpg"
        }
        
        user = UserFactory.build() # Not saved
        # Mock super().populate_user behavior
        user.username = "john" 
        
        # We need to mock super().populate_user call, but since we can't easily mock super() in this context without complex patching,
        # we will assume the method modifies the user object passed or returned.
        # Actually, populate_user returns the user.
        
        # Let's just test the logic inside populate_user by calling it.
        # We need to patch super() or just instantiate the adapter and call it.
        # Since it inherits from DefaultSocialAccountAdapter, we can rely on it.
        
        user = adapter.populate_user(request, sociallogin, {})
        
        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.avatar_url == "http://example.com/avatar.jpg"

    def test_save_user(self):
        adapter = SocialAccountAdapter()
        request = Mock()
        sociallogin = Mock(spec=SocialLogin)
        sociallogin.account = Mock(spec=SocialAccount)
        sociallogin.account.uid = "12345"
        sociallogin.account.extra_data = {
            "sub": "12345",
            "email": "test@10code.es"
        }
        
        user = UserFactory()
        # Mock super().save_user to return the user
        # We can't easily mock super() here. 
        # Instead, we can check if GoogleProfile is created after save_user is called.
        # But save_user calls super().save_user which saves the user.
        
        # To properly test this without mocking super, we can just call it.
        # DefaultSocialAccountAdapter.save_user saves the user.
        
        saved_user = adapter.save_user(request, sociallogin, form=None)
        
        assert GoogleProfile.objects.filter(user=saved_user).exists()
        profile = saved_user.google_profile
        assert profile.google_id == "12345"
        assert profile.email == "test@10code.es"
