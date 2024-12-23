from rest_framework import serializers
from core.models.product import Product, ProductType, ProductInventory, Material, MaterialType, MaterialInventory

class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = ['id', 'product_type']

class ProductSerializer(serializers.ModelSerializer):
    product_type_detail = ProductTypeSerializer(source='product_type', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'product_type', 'product_type_detail', 'cost', 'measure', 'product', 'active']

class ProductInventorySerializer(serializers.ModelSerializer):
    product_detail = ProductSerializer(source='product', read_only=True)

    class Meta:
        model = ProductInventory
        fields = ['id', 'product', 'product_detail', 'company_location_link', 
                 'stock', 'in_progress', 'stock_level_warning']

class MaterialTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialType
        fields = ['id', 'material_type']

class MaterialSerializer(serializers.ModelSerializer):
    material_type_detail = MaterialTypeSerializer(source='material_type', read_only=True)

    class Meta:
        model = Material
        fields = ['id', 'material_type', 'material_type_detail', 'cost', 'measure', 
                 'material', 'water_low', 'water_high', 'mix_low', 'mix_high', 
                 'taps', 'lower_spec', 'upper_spec', 'std_water', 'std_mix']

class MaterialInventorySerializer(serializers.ModelSerializer):
    material_detail = MaterialSerializer(source='material', read_only=True)

    class Meta:
        model = MaterialInventory
        fields = ['id', 'material', 'material_detail', 'company_location_link',
                 'stock', 'in_progress', 'stock_level_warning']

class InventoryUpdateSerializer(serializers.Serializer):
    value = serializers.IntegerField()
    notes = serializers.CharField(required=False, allow_blank=True)
