from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Avg, Count, F, Q
from django.db.models.functions import TruncDate, TruncMonth
from django.utils import timezone
from datetime import timedelta

from core.models.production import ProductionOrder, ProductionOrderMaterialLink
from core.models.product import ProductInventory, MaterialInventory
from .serializers import (
    ProductionSummarySerializer,
    InventorySummarySerializer,
    MaterialUsageSerializer
)

class ReportViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def production_summary(self, request):
        period = request.query_params.get('period', 'daily')
        days = int(request.query_params.get('days', 30))
        start_date = timezone.now().date() - timedelta(days=days)

        trunc_func = TruncDate('fill_date') if period == 'daily' else TruncMonth('fill_date')

        summary = ProductionOrder.objects.filter(
            fill_date__gte=start_date
        ).annotate(
            date=trunc_func
        ).values('date').annotate(
            total_orders=Count('id'),
            total_quantity=Sum('quantity_ordered'),
            completed_orders=Count('id', filter=Q(active=False)),
            completion_rate=Count('id', filter=Q(active=False)) * 100.0 / Count('id')
        ).order_by('date')

        serializer = ProductionSummarySerializer(summary, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def inventory_status(self, request):
        location = request.query_params.get('location')
        query = ProductInventory.objects.all()
        
        if location:
            query = query.filter(company_location_link=location)

        inventory = query.annotate(
            product_name=F('product__product'),
            low_stock_warning=F('stock') <= F('stock_level_warning')
        ).values(
            'product_id',
            'product_name',
            'stock',
            'in_progress',
            'low_stock_warning'
        )

        serializer = InventorySummarySerializer(inventory, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def material_usage(self, request):
        start_date = request.query_params.get(
            'start_date',
            (timezone.now() - timedelta(days=30)).date().isoformat()
        )
        
        usage = ProductionOrderMaterialLink.objects.filter(
            production_order__fill_date__gte=start_date
        ).values(
            material_id=F('material__id'),
            material_name=F('material__material')
        ).annotate(
            total_used=Sum('quantity'),
            average_per_order=Avg('quantity'),
            total_cost=Sum(F('quantity') * F('material__cost'))
        ).order_by('-total_used')

        serializer = MaterialUsageSerializer(usage, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def low_stock_alerts(self, request):
        location = request.query_params.get('location')
        query = ProductInventory.objects.filter(stock__lte=F('stock_level_warning'))
        
        if location:
            query = query.filter(company_location_link=location)

        alerts = query.annotate(
            product_name=F('product__product')
        ).values(
            'product_id',
            'product_name',
            'stock',
            'stock_level_warning'
        )

        return Response(alerts)