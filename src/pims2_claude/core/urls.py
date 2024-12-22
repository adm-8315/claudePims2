from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import inventory

router = DefaultRouter()
router.register(r'product-inventory', inventory.ProductInventoryViewSet)
router.register(r'material-inventory', inventory.MaterialInventoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]