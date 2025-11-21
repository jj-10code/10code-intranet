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
        request.META = {"HTTP_X_FORWARDED_FOR": "127.0.0.1"}
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
        sociallogin.user = UserFactory.build()
        
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
        # Use create to have a saved user, as sociallogin.save() is mocked
        sociallogin.user = UserFactory()
        
        # Mock save to do nothing (user already saved)
        sociallogin.save = Mock()
        
        saved_user = adapter.save_user(request, sociallogin, form=None)
        
        assert GoogleProfile.objects.filter(user=saved_user).exists()
        profile = saved_user.google_profile
        assert profile.google_id == "12345"
        assert profile.email == "test@10code.es"
