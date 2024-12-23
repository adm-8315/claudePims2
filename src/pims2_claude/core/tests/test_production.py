import pytest
from django.urls import reverse
from rest_framework import status
from core.models.production import ProductionOrder, ProductionOrderTemplate
from core.models.product import Product, ProductType

@pytest.fixture
def create_product(db):
    product_type = ProductType.objects.create(product_type='Test Type')
    return Product.objects.create(
        product_type=product_type,
        product='Test Product',
        cost=100.00,
        active=True
    )

@pytest.fixture
def create_production_order(db, create_user, create_product):
    return ProductionOrder.objects.create(
        product=create_product,
        quantity_ordered=100,
        notes='Test Order',
        user=create_user(),
        active=True
    )

@pytest.fixture
def create_template(db, create_user, create_product):
    return ProductionOrderTemplate.objects.create(
        product=create_product,
        notes='Test Template',
        user=create_user(),
        active=True
    )

@pytest.mark.django_db
class TestProductionOrder:
    def test_create_production_order(self, authenticated_client, create_product):
        url = reverse('productionorder-list')
        data = {
            'product': create_product.id,
            'quantity_ordered': 100,
            'notes': 'Test Order'
        }
        
        response = authenticated_client.post(url, data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['quantity_ordered'] == 100
        assert response.data['notes'] == 'Test Order'

    def test_list_production_orders(self, authenticated_client, create_production_order):
        url = reverse('productionorder-list')
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1

    def test_complete_production_order(self, authenticated_client, create_production_order):
        url = reverse('productionorder-complete', kwargs={'pk': create_production_order.id})
        data = {'quantity': 50}
        
        response = authenticated_client.post(url, data)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['quantity_filled'] == 50
        assert response.data['active'] == True  # Still active as not fully completed

    def test_filter_production_orders(self, authenticated_client, create_production_order):
        url = f"{reverse('productionorder-list')}?active=true"
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1

        url = f"{reverse('productionorder-list')}?active=false"
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 0

@pytest.mark.django_db
class TestProductionOrderTemplate:
    def test_create_from_template(self, authenticated_client, create_template):
        url = reverse('productionordertemplate-create-order', kwargs={'pk': create_template.id})
        data = {'quantity': 150}
        
        response = authenticated_client.post(url, data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['quantity_ordered'] == 150
        assert response.data['product'] == create_template.product.id

    def test_create_template(self, authenticated_client, create_product):
        url = reverse('productionordertemplate-list')
        data = {
            'product': create_product.id,
            'notes': 'New Template',
        }
        
        response = authenticated_client.post(url, data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['notes'] == 'New Template'
        assert response.data['product'] == create_product.id