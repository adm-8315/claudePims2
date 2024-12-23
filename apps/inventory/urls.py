from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    # List views
    path('items/', views.ItemListView.as_view(), name='item-list'),
    path('materials/', views.MaterialListView.as_view(), name='material-list'),
    path('products/', views.ProductListView.as_view(), name='product-list'),
    
    # Detail views
    path('materials/<int:pk>/', views.MaterialDetailView.as_view(), name='material-detail'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    
    # Transaction views
    path('materials/transaction/new/', views.MaterialTransactionCreateView.as_view(), name='material-transaction-create'),
    path('products/transaction/new/', views.ProductTransactionCreateView.as_view(), name='product-transaction-create'),
]
