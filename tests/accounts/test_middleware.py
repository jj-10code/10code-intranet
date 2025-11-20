import pytest
from django.conf import settings
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory, override_settings
from django.utils import timezone
from apps.accounts.middleware import ActivityTrackingMiddleware
from apps.accounts.models import User

@pytest.mark.django_db
class TestSessionConfiguration:
    def test_session_settings(self):
        """Verify session configuration settings."""
        assert settings.SESSION_COOKIE_AGE == 28800
        assert settings.SESSION_SAVE_EVERY_REQUEST is True
        assert settings.SESSION_ENGINE == "django.contrib.sessions.backends.cache"

@pytest.mark.django_db
class TestActivityTrackingMiddleware:
    def test_activity_updates_session(self):
        """Test that middleware updates last_activity in session."""
        factory = RequestFactory()
        request = factory.get('/')
        
        # Setup session
        middleware = SessionMiddleware(lambda r: None)
        middleware.process_request(request)
        request.session.save()
        
        # Setup user
        user = User.objects.create_user(username='testuser', email='test@example.com', password='password')
        request.user = user
        
        # Run middleware
        tracking_middleware = ActivityTrackingMiddleware(lambda r: None)
        tracking_middleware(request)
        
        assert 'last_activity' in request.session
        # Verify it's a valid ISO format date
        last_activity = request.session['last_activity']
        assert timezone.datetime.fromisoformat(last_activity)

    def test_anonymous_user_no_tracking(self):
        """Test that anonymous users are not tracked."""
        factory = RequestFactory()
        request = factory.get('/')
        
        # Setup session
        middleware = SessionMiddleware(lambda r: None)
        middleware.process_request(request)
        request.session.save()
        
        # Anonymous user
        from django.contrib.auth.models import AnonymousUser
        request.user = AnonymousUser()
        
        # Run middleware
        tracking_middleware = ActivityTrackingMiddleware(lambda r: None)
        tracking_middleware(request)
        
        assert 'last_activity' not in request.session
