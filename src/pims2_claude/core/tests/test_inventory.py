import pytest
from django.urls import reverse
from rest_framework import status
from core.models.product import Product, ProductType, ProductInventory
from core.models.company import CompanyLocationLink

@pytest.fixture
def create_inventory(db, create_product):
    return ProductInventory.objects.create(
        product=create_product,
        company_location_link=1,  # You might want to create a proper CompanyLocationLink
        stock=100,
        stock_level_warning=20
    )

@pytest.mark.django_db
class TestInventoryManagement:
    def test_list_inventory(self, authenticated_client, create_inventory):
        url = reverse('productinventory-list')
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['stock'] == 100

    def test_adjust_stock(self, authenticated_client, create_inventory):
        url = reverse('productinventory-adjust-stock', kwargs={'pk': create_inventory.id})
        data = {
            'value': 50,
            'notes': 'Stock adjustment'
        }
        
        response = authenticated_client.post(url, data)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['stock'] == 150  # 100 + 50

    def test_receive_stock(self, authenticated_client, create_inventory):
        url = reverse('productinventory-receive', kwargs={'pk': create_inventory.id})
        data = {
            'value': 25,
            'notes': 'Stock received'
        }
        
        response = authenticated_client.post(url, data)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['stock'] == 125  # 100 + 25

    def test_consume_stock(self, authenticated_client, create_inventory):
        url = reverse('productinventory-consume', kwargs={'pk': create_inventory.id})
        data = {
            'value': 30,
            'notes': 'Stock consumed'
        }
        
        response = authenticated_client.post(url, data)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['stock'] == 70  # 100 - 30

    def test_prevent_negative_stock(self, authenticated_client, create_inventory):
        url = reverse('productinventory-consume', kwargs={'pk': create_inventory.id})
        data = {
            'value': 150,  # Trying to consume more than available
            'notes': 'Should fail'
        }
        
        response = authenticated_client.post(url, data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
        # Verify stock hasn't changed
        url = reverse('productinventory-list')
        response = authenticated_client.get(url)
        assert response.data['results'][0]['stock'] == 100

    def test_filter_by_location(self, authenticated_client, create_inventory):
        url = f"{reverse('productinventory-list')}?location=1"
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1

        url = f"{reverse('productinventory-list')}?location=999"  # Non-existent location
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 0