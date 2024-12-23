from rest_framework import serializers
from core.models.scheduling import BatchSchedule, BatchAssignment, MixingRule
from core.serializers.production import ProductionOrderSerializer

class MixingRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MixingRule
        fields = ['id', 'product', 'mixer', 'minimum_batch', 'maximum_batch',
                 'ideal_batch', 'mixing_time', 'cleanup_time', 'notes']
        
    def validate(self, data):
        if data['minimum_batch'] > data['maximum_batch']:
            raise serializers.ValidationError({
                'minimum_batch': 'Cannot be greater than maximum batch'
            })
        if data['ideal_batch'] < data['minimum_batch'] or \
           data['ideal_batch'] > data['maximum_batch']:
            raise serializers.ValidationError({
                'ideal_batch': 'Must be between minimum and maximum batch sizes'
            })
        return data

class BatchScheduleSerializer(serializers.ModelSerializer):
    available_capacity = serializers.SerializerMethodField()
    
    class Meta:
        model = BatchSchedule
        fields = ['id', 'date', 'mixer', 'capacity_reserved',
                 'available_capacity', 'notes', 'created_at', 'updated_at']
        read_only_fields = ['capacity_reserved', 'created_at', 'updated_at']
    
    def get_available_capacity(self, obj):
        return obj.mixer.mixer_max - obj.capacity_reserved

class BatchAssignmentSerializer(serializers.ModelSerializer):
    production_order_detail = ProductionOrderSerializer(
        source='production_order', read_only=True
    )
    mixing_rule = serializers.SerializerMethodField()
    
    class Meta:
        model = BatchAssignment
        fields = ['id', 'batch_schedule', 'production_order',
                 'production_order_detail', 'priority', 'status',
                 'quantity', 'sequence_number', 'start_time',
                 'completion_time', 'notes', 'mixing_rule',
                 'created_at', 'updated_at']
        read_only_fields = ['sequence_number', 'created_at', 'updated_at']
    
    def get_mixing_rule(self, obj):
        rule = MixingRule.objects.filter(
            product=obj.production_order.product,
            mixer=obj.batch_schedule.mixer
        ).first()
        if rule:
            return MixingRuleSerializer(rule).data
        return None
    
    def validate(self, data):
        # Validate mixing rule exists
        rule = MixingRule.objects.filter(
            product=data['production_order'].product,
            mixer=data['batch_schedule'].mixer
        ).first()
        if not rule:
            raise serializers.ValidationError(
                'No mixing rule defined for this product and mixer combination'
            )
        
        # Validate batch size
        if data['quantity'] < rule.minimum_batch:
            raise serializers.ValidationError({
                'quantity': f'Batch size must be at least {rule.minimum_batch}'
            })
        if data['quantity'] > rule.maximum_batch:
            raise serializers.ValidationError({
                'quantity': f'Batch size cannot exceed {rule.maximum_batch}'
            })
        
        # Validate available capacity
        schedule = data['batch_schedule']
        current_reserved = schedule.capacity_reserved
        if self.instance:
            current_reserved -= self.instance.quantity
        
        if current_reserved + data['quantity'] > schedule.mixer.mixer_max:
            raise serializers.ValidationError(
                'Assignment would exceed mixer capacity'
            )
        
        return data

class ScheduleSummarySerializer(serializers.Serializer):
    date = serializers.DateField()
    mixer = serializers.IntegerField()
    mixer_name = serializers.CharField()
    total_capacity = serializers.IntegerField()
    reserved_capacity = serializers.IntegerField()
    available_capacity = serializers.IntegerField()
    batch_count = serializers.IntegerField()
    status_summary = serializers.DictField()
