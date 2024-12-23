from rest_framework import serializers
from core.models.production import (
    ProductionOrder, ProductionOrderMaterialLink, ProductionOrderSchedule,
    Form, FurnacePattern, ProductionOrderTemplate
)
from core.serializers.inventory import ProductSerializer, MaterialSerializer

class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        fields = ['id', 'form_tag', 'form_location', 'form_quantity', 
                 'form_pieces', 'notes']

class FurnacePatternSerializer(serializers.ModelSerializer):
    class Meta:
        model = FurnacePattern
        fields = ['id', 'furnace', 'furnace_pattern', 'pattern_description',
                 'pattern_temperature', 'pattern_time']

class ProductionOrderMaterialLinkSerializer(serializers.ModelSerializer):
    material_detail = MaterialSerializer(source='material', read_only=True)

    class Meta:
        model = ProductionOrderMaterialLink
        fields = ['id', 'material', 'material_detail', 'quantity', 'water',
                 'mix_time', 'vibration_type', 'vibration_time']

class ProductionOrderScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionOrderSchedule
        fields = ['id', 'production_order', 'pour_date', 'strip_date',
                 'fire_date', 'quantity', 'active']
        read_only_fields = ['production_order']

class ProductionOrderSerializer(serializers.ModelSerializer):
    product_detail = ProductSerializer(source='product', read_only=True)
    form_detail = FormSerializer(source='form', read_only=True)
    furnace_pattern_detail = FurnacePatternSerializer(source='furnace_pattern', read_only=True)
    materials = ProductionOrderMaterialLinkSerializer(source='productionordermateriallink_set', many=True, read_only=True)
    schedule = ProductionOrderScheduleSerializer(source='productionorderschedule_set', many=True, read_only=True)

    class Meta:
        model = ProductionOrder
        fields = ['id', 'product', 'product_detail', 'quantity_ordered',
                 'quantity_filled', 'fill_date', 'notes', 'form', 'form_detail',
                 'taps', 'lower_spec', 'upper_spec', 'furnace_pattern',
                 'furnace_pattern_detail', 'user', 'last_edit', 'active',
                 'materials', 'schedule']
        read_only_fields = ['user', 'last_edit']

    def validate(self, data):
        # Ensure quantity_ordered is positive
        if 'quantity_ordered' in data and data['quantity_ordered'] <= 0:
            raise serializers.ValidationError({
                'quantity_ordered': 'Must be greater than zero'
            })
        return data

class ProductionOrderTemplateSerializer(serializers.ModelSerializer):
    product_detail = ProductSerializer(source='product', read_only=True)
    form_detail = FormSerializer(source='form', read_only=True)
    furnace_pattern_detail = FurnacePatternSerializer(source='furnace_pattern', read_only=True)

    class Meta:
        model = ProductionOrderTemplate
        fields = ['id', 'product', 'product_detail', 'notes', 'form',
                 'form_detail', 'taps', 'lower_spec', 'upper_spec',
                 'furnace_pattern', 'furnace_pattern_detail', 'user',
                 'last_edit', 'active']
        read_only_fields = ['user', 'last_edit']
