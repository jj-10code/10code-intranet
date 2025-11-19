import pytest
from rest_framework.test import APIClient
from tests.factories import UserFactory

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user():
    return UserFactory()
