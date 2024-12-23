import pytest
from django.urls import reverse
from rest_framework import status

@pytest.mark.django_db
class TestAuthentication:
    def test_login_success(self, api_client, create_user):
        user = create_user(username='testuser', password='testpass123')
        url = reverse('auth-login')
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        
        response = api_client.post(url, data)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'token' in response.data
        assert response.data['user']['username'] == 'testuser'

    def test_login_invalid_credentials(self, api_client):
        url = reverse('auth-login')
        data = {
            'username': 'wronguser',
            'password': 'wrongpass'
        }
        
        response = api_client.post(url, data)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_protected_endpoint_without_auth(self, api_client):
        url = reverse('productionorder-list')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_protected_endpoint_with_auth(self, authenticated_client):
        url = reverse('productionorder-list')
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK

    def test_inactive_user_login(self, api_client, create_user):
        user = create_user(username='inactive', password='test123')
        user.active = False
        user.save()

        url = reverse('auth-login')
        data = {
            'username': 'inactive',
            'password': 'test123'
        }
        
        response = api_client.post(url, data)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED