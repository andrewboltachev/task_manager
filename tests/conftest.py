import pytest
from rest_framework.test import APIClient

from tests.factories import UserFactory


@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user():
    """Creates a generic user"""
    return UserFactory()

@pytest.fixture
def auth_client(user):
    """
    Returns an APIClient that is ALREADY logged in.
    """
    client = APIClient()
    # Force authenticate skips the JWT ceremony - faster for logic tests
    client.force_authenticate(user=user)
    return client
