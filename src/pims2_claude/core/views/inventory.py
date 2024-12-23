from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.utils import timezone

from core.models.product import ProductInventory, MaterialInventory
from core.serializers.inventory import (
    ProductInventorySerializer, MaterialInventorySerializer,
    InventoryUpdateSerializer
)

class BaseInventoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset
        location = self.request.query_params.get('location', None)
        if location:
            queryset = queryset.filter(company_location_link=location)
        return queryset

    @transaction.atomic
    def update_inventory(self, instance, value, transaction_type, notes=None):
        # Update stock level
        instance.stock += value
        if instance.stock < 0:
            return Response(
                {'error': 'Insufficient stock'},
                status=status.HTTP_400_BAD_REQUEST
            )
        instance.save()

        # Create transaction record
        self.transaction_model.objects.create(
            inventory=instance,
            transaction_type=transaction_type,
            value=value,
            user=self.request.user,
            timestamp=timezone.now(),
            notes=notes
        )

        return Response(self.get_serializer(instance).data)

class ProductInventoryViewSet(BaseInventoryViewSet):
    queryset = ProductInventory.objects.all()
    serializer_class = ProductInventorySerializer

    @action(detail=True, methods=['post'])
    def adjust_stock(self, request, pk=None):
        inventory = self.get_object()
        serializer = InventoryUpdateSerializer(data=request.data)
        if serializer.is_valid():
            return self.update_inventory(
                inventory,
                serializer.validated_data['value'],
                'adjustment',
                serializer.validated_data.get('notes')
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def receive(self, request, pk=None):
        inventory = self.get_object()
        serializer = InventoryUpdateSerializer(data=request.data)
        if serializer.is_valid():
            return self.update_inventory(
                inventory,
                abs(serializer.validated_data['value']),  # Ensure positive
                'receive',
                serializer.validated_data.get('notes')
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def consume(self, request, pk=None):
        inventory = self.get_object()
        serializer = InventoryUpdateSerializer(data=request.data)
        if serializer.is_valid():
            return self.update_inventory(
                inventory,
                -abs(serializer.validated_data['value']),  # Ensure negative
                'consume',
                serializer.validated_data.get('notes')
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MaterialInventoryViewSet(BaseInventoryViewSet):
    queryset = MaterialInventory.objects.all()
    serializer_class = MaterialInventorySerializer

    @action(detail=True, methods=['post'])
    def adjust_stock(self, request, pk=None):
        inventory = self.get_object()
        serializer = InventoryUpdateSerializer(data=request.data)
        if serializer.is_valid():
            return self.update_inventory(
                inventory,
                serializer.validated_data['value'],
                'adjustment',
                serializer.validated_data.get('notes')
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def receive(self, request, pk=None):
        inventory = self.get_object()
        serializer = InventoryUpdateSerializer(data=request.data)
        if serializer.is_valid():
            return self.update_inventory(
                inventory,
                abs(serializer.validated_data['value']),
                'receive',
                serializer.validated_data.get('notes')
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def consume(self, request, pk=None):
        inventory = self.get_object()
        serializer = InventoryUpdateSerializer(data=request.data)
        if serializer.is_valid():
            return self.update_inventory(
                inventory,
                -abs(serializer.validated_data['value']),
                'consume',
                serializer.validated_data.get('notes')
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
