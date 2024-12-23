from django.urls import path
from . import views

app_name = 'production'

urlpatterns = [
    # Production Orders
    path('orders/', views.ProductionOrderListView.as_view(), name='order_list'),
    path('orders/create/', views.ProductionOrderCreateView.as_view(), name='order_create'),
    path('orders/<int:pk>/', views.ProductionOrderDetailView.as_view(), name='order_detail'),
    path('orders/<int:pk>/edit/', views.ProductionOrderUpdateView.as_view(), name='order_edit'),
    
    # Production Order Scheduling
    path('orders/<int:order_pk>/schedule/', views.ProductionOrderScheduleCreateView.as_view(), name='schedule_create'),
]
