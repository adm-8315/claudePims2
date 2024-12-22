from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import inventory, production

router = DefaultRouter()

# Inventory routes
router.register(r'product-inventory', inventory.ProductInventoryViewSet)
router.register(r'material-inventory', inventory.MaterialInventoryViewSet)

# Production routes
router.register(r'production-orders', production.ProductionOrderViewSet)
router.register(r'production-templates', production.ProductionOrderTemplateViewSet)
router.register(r'forms', production.FormViewSet)
router.register(r'furnace-patterns', production.FurnacePatternViewSet)

urlpatterns = [
    path('', include(router.urls)),
]