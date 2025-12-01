import pytest
from django.urls import reverse
from rest_framework import status

from tests.factories import TaskFactory, UserFactory


@pytest.mark.django_db
class TestTaskOperations:
    
    def test_list_tasks(self, auth_client):
        # Create 3 tasks
        TaskFactory.create_batch(3)
        
        url = reverse('task-list') # Standard Router name
        response = auth_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 3 # Pagination enabled by default

    def test_create_task(self, auth_client, user):
        url = reverse('task-list')
        data = {'title': 'Buy Milk', 'description': 'Urgent'}
        
        response = auth_client.post(url, data)
        
        assert response.status_code == status.HTTP_201_CREATED
        # Check that creator was set automatically to the logged-in user
        assert response.data['creator']['id'] == user.id

    def test_update_task_permission(self, api_client):
        """
        User A creates task. User B tries to update it. Should Fail.
        """
        owner = UserFactory()
        attacker = UserFactory()
        task = TaskFactory(creator=owner)
        
        # Log in as Attacker
        api_client.force_authenticate(user=attacker)
        
        url = reverse('task-detail', args=[task.id])
        data = {'title': 'Hacked'}
        
        response = api_client.patch(url, data)
        
        # Depending on your permissions (IsEditorOrReadOnly), this might be 403 or 200
        # If IsEditorOrReadOnly allows READ but restricts WRITE:
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_task_filtering(self, auth_client):
        # Create tasks with specific statuses
        TaskFactory(status='new')
        TaskFactory(status='completed')
        
        url = reverse('task-list')
        response = auth_client.get(f"{url}?status=new")
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
        assert response.data['results'][0]['status'] == 'new'
