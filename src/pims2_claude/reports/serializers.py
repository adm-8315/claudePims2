from rest_framework import serializers

class ProductionSummarySerializer(serializers.Serializer):
    date = serializers.DateField()
    total_orders = serializers.IntegerField()
    total_quantity = serializers.IntegerField()
    completed_orders = serializers.IntegerField()
    completion_rate = serializers.FloatField()

class InventorySummarySerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    product_name = serializers.CharField()
    total_stock = serializers.IntegerField()
    in_progress = serializers.IntegerField()
    low_stock_warning = serializers.BooleanField()

class MaterialUsageSerializer(serializers.Serializer):
    material_id = serializers.IntegerField()
    material_name = serializers.CharField()
    total_used = serializers.FloatField()
    average_per_order = serializers.FloatField()
    total_cost = serializers.DecimalField(max_digits=10, decimal_places=2)