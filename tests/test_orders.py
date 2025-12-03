import pytest
from django.urls import reverse
from rest_framework import status

from tests.factories import OrderFactory, UserFactory


@pytest.mark.django_db
class TestOrderOperations:
    
    def test_list_orders(self, auth_client):
        # Create 3 tasks
        OrderFactory.create_batch(3)
        
        url = reverse('order-list') # Standard Router name
        response = auth_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 3 # Pagination enabled by default

    def test_create_order(self, auth_client, user):
        url = reverse('order-list')
        data = {'title': 'Buy Milk', 'description': 'Urgent'}
        
        response = auth_client.post(url, data)
        
        assert response.status_code == status.HTTP_201_CREATED
        # Check that creator was set automatically to the logged-in user
        assert response.data['creator']['id'] == user.id

    def test_update_order_permission(self, api_client):
        """
        User A creates order. User B tries to update it. Should Fail.
        """
        owner = UserFactory()
        attacker = UserFactory()
        order = OrderFactory(creator=owner)
        
        # Log in as Attacker
        api_client.force_authenticate(user=attacker)
        
        url = reverse('order-detail', args=[order.id])
        data = {'title': 'Hacked'}
        
        response = api_client.patch(url, data)
        
        # Depending on your permissions (IsEditorOrReadOnly), this might be 403 or 200
        # If IsEditorOrReadOnly allows READ but restricts WRITE:
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_order_filtering(self, auth_client):
        # Create tasks with specific statuses
        OrderFactory(status='new')
        OrderFactory(status='completed')
        
        url = reverse('order-list')
        response = auth_client.get(f"{url}?status=new")
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
        assert response.data['results'][0]['status'] == 'new'
