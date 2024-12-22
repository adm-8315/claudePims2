import pytest
from django.urls import reverse
from rest_framework import status
from datetime import datetime, timedelta
from django.utils import timezone
from core.models.production import ProductionOrder
from core.models.product import ProductInventory, Product, ProductType

@pytest.fixture
def create_production_data(db, create_user, create_product):
    # Create multiple production orders for testing
    orders = [
        ProductionOrder.objects.create(
            product=create_product,
            quantity_ordered=100,
            quantity_filled=100 if i % 2 == 0 else 50,  # Some complete, some partial
            fill_date=timezone.now().date() - timedelta(days=i),
            user=create_user(),
            active=i % 2 != 0  # Some active, some inactive
        ) for i in range(5)
    ]
    return orders

@pytest.fixture
def create_inventory_data(db, create_product):
    # Create inventory records for testing
    return ProductInventory.objects.create(
        product=create_product,
        company_location_link=1,
        stock=50,
        in_progress=20,
        stock_level_warning=100  # This will trigger low stock warning
    )

@pytest.mark.django_db
class TestReports:
    def test_production_summary(self, authenticated_client, create_production_data):
        url = reverse('report-production-summary')
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.data
        assert len(data) > 0
        assert 'total_orders' in data[0]
        assert 'completion_rate' in data[0]

    def test_inventory_status(self, authenticated_client, create_inventory_data):
        url = reverse('report-inventory-status')
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.data
        assert len(data) > 0
        assert data[0]['low_stock_warning'] == True  # Based on our fixture data

    def test_low_stock_alerts(self, authenticated_client, create_inventory_data):
        url = reverse('report-low-stock-alerts')
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.data
        assert len(data) > 0  # Should have our low stock item

    def test_production_summary_with_period(self, authenticated_client, create_production_data):
        url = f"{reverse('report-production-summary')}?period=monthly&days=60"
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) > 0

    def test_inventory_status_with_location(self, authenticated_client, create_inventory_data):
        url = f"{reverse('report-inventory-status')}?location=1"
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1  # Should only show inventory for location 1