import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

# This marker ensures DB access is allowed
@pytest.mark.django_db
def test_register_user(api_client):
    url = reverse('auth_register') # Ensure this matches your urls.py name
    data = {
        'username': 'newuser',
        'email': 'new@test.com',
        'password': 'strong_password_123',
        'first_name': 'Test',
    }
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.count() == 1

@pytest.mark.django_db
def test_get_jwt_token(api_client, user):
    # 'user' fixture has password 'password123' (from factory)
    url = reverse('token_obtain_pair')
    data = {
        'username': user.username,
        'password': 'password123'
    }
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_200_OK
    assert 'access' in response.data
    assert 'refresh' in response.data
