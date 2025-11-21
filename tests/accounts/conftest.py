import pytest
from django.test import RequestFactory
from tests.factories import UserFactory, RoleFactory, GoogleProfileFactory

@pytest.fixture
def user_factory():
    return UserFactory

@pytest.fixture
def role_factory():
    return RoleFactory

@pytest.fixture
def google_profile_factory():
    return GoogleProfileFactory

@pytest.fixture
def request_factory():
    return RequestFactory()

@pytest.fixture(autouse=True)
def mock_redis_cache(settings):
    """
    Override cache settings to use LocMemCache for all tests.
    This avoids connecting to a real Redis instance.
    """
    settings.CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "unique-snowflake",
        }
    }
    settings.SESSION_ENGINE = "django.contrib.sessions.backends.cache"
