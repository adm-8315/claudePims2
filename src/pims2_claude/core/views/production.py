from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as filters
from django.db import transaction
from django.utils import timezone

from core.models.production import (
    ProductionOrder, ProductionOrderMaterialLink, ProductionOrderSchedule,
    ProductionOrderTemplate, Form, FurnacePattern
)
from core.serializers.production import (
    ProductionOrderSerializer, ProductionOrderMaterialLinkSerializer,
    ProductionOrderScheduleSerializer, ProductionOrderTemplateSerializer,
    FormSerializer, FurnacePatternSerializer
)

class ProductionOrderFilter(filters.FilterSet):
    start_date = filters.DateFilter(field_name='fill_date', lookup_expr='gte')
    end_date = filters.DateFilter(field_name='fill_date', lookup_expr='lte')
    product = filters.NumberFilter(field_name='product__id')
    active = filters.BooleanFilter()

    class Meta:
        model = ProductionOrder
        fields = ['product', 'active', 'start_date', 'end_date']

class ProductionOrderViewSet(viewsets.ModelViewSet):
    queryset = ProductionOrder.objects.all()
    serializer_class = ProductionOrderSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = ProductionOrderFilter
    search_fields = ['product__product', 'notes']
    ordering_fields = ['fill_date', 'last_edit', 'quantity_ordered']
    ordering = ['-last_edit']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    @transaction.atomic
    def add_materials(self, request, pk=None):
        production_order = self.get_object()
        serializer = ProductionOrderMaterialLinkSerializer(
            data=request.data, many=True
        )
        
        if serializer.is_valid():
            serializer.save(production_order=production_order)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    @transaction.atomic
    def schedule(self, request, pk=None):
        production_order = self.get_object()
        serializer = ProductionOrderScheduleSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(production_order=production_order)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        production_order = self.get_object()
        quantity = request.data.get('quantity')

        if not quantity or quantity <= 0:
            return Response(
                {'error': 'Valid quantity required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        production_order.quantity_filled += quantity
        production_order.fill_date = timezone.now().date()
        if production_order.quantity_filled >= production_order.quantity_ordered:
            production_order.active = False
        production_order.save()

        return Response(ProductionOrderSerializer(production_order).data)

class ProductionOrderTemplateFilter(filters.FilterSet):
    product = filters.NumberFilter(field_name='product__id')
    active = filters.BooleanFilter()

    class Meta:
        model = ProductionOrderTemplate
        fields = ['product', 'active']

class ProductionOrderTemplateViewSet(viewsets.ModelViewSet):
    queryset = ProductionOrderTemplate.objects.all()
    serializer_class = ProductionOrderTemplateSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = ProductionOrderTemplateFilter
    search_fields = ['product__product', 'notes']
    ordering_fields = ['last_edit']
    ordering = ['-last_edit']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    @transaction.atomic
    def create_order(self, request, pk=None):
        template = self.get_object()
        quantity = request.data.get('quantity')
        
        if not quantity or quantity <= 0:
            return Response(
                {'error': 'Valid quantity required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create new production order from template
        production_order = ProductionOrder.objects.create(
            product=template.product,
            quantity_ordered=quantity,
            notes=template.notes,
            form=template.form,
            taps=template.taps,
            lower_spec=template.lower_spec,
            upper_spec=template.upper_spec,
            furnace_pattern=template.furnace_pattern,
            user=self.request.user
        )

        return Response(
            ProductionOrderSerializer(production_order).data,
            status=status.HTTP_201_CREATED
        )

class FormViewSet(viewsets.ModelViewSet):
    queryset = Form.objects.all()
    serializer_class = FormSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['form_tag', 'form_location', 'notes']
    ordering_fields = ['form_tag', 'form_location']
    ordering = ['form_tag']

class FurnacePatternViewSet(viewsets.ModelViewSet):
    queryset = FurnacePattern.objects.all()
    serializer_class = FurnacePatternSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['furnace_pattern', 'pattern_description']
    ordering_fields = ['furnace_pattern', 'pattern_temperature']
    ordering = ['furnace_pattern']