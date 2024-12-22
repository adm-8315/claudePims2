from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Count, Q, F
from django.db import transaction
from django.utils import timezone
from datetime import timedelta

from core.models.scheduling import BatchSchedule, BatchAssignment, MixingRule
from core.serializers.scheduling import (
    BatchScheduleSerializer, BatchAssignmentSerializer,
    MixingRuleSerializer, ScheduleSummarySerializer
)

class BatchAssignmentViewSet(viewsets.ModelViewSet):
    queryset = BatchAssignment.objects.all()
    serializer_class = BatchAssignmentSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['batch_schedule', 'production_order', 'status', 'priority']
    
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        assignment = self.get_object()
        new_status = request.data.get('status')
        
        if new_status not in dict(BatchAssignment.STATUS_CHOICES):
            return Response(
                {'error': 'Invalid status'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        with transaction.atomic():
            if new_status == 'in_progress' and not assignment.start_time:
                assignment.start_time = timezone.now().time()
            elif new_status == 'completed' and not assignment.completion_time:
                assignment.completion_time = timezone.now().time()
                
                # Update production order quantity filled
                assignment.production_order.quantity_filled += assignment.quantity
                if assignment.production_order.quantity_filled >= assignment.production_order.quantity_ordered:
                    assignment.production_order.active = False
                assignment.production_order.save()
            
            assignment.status = new_status
            assignment.save()
        
        return Response(self.get_serializer(assignment).data)
    
    @action(detail=False, methods=['post'])
    def optimize_schedule(self, request):
        """Automatically optimize batch assignments for a given date range."""
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        mixer_id = request.data.get('mixer')
        
        if not all([start_date, end_date]):
            return Response(
                {'error': 'start_date and end_date are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get unscheduled production orders
        unscheduled_orders = ProductionOrder.objects.filter(
            active=True,
            quantity_ordered__gt=F('quantity_filled')
        ).order_by('priority', 'created_at')
        
        # Get available batch schedules
        schedules = BatchSchedule.objects.filter(
            date__range=[start_date, end_date]
        )
        if mixer_id:
            schedules = schedules.filter(mixer_id=mixer_id)
        
        optimized_assignments = []
        
        for order in unscheduled_orders:
            remaining_quantity = order.quantity_ordered - order.quantity_filled
            
            # Get mixing rule for this product
            mixing_rule = MixingRule.objects.filter(
                product=order.product,
                mixer__in=schedules.values_list('mixer', flat=True)
            ).first()
            
            if not mixing_rule:
                continue
            
            # Calculate number of batches needed
            batch_size = mixing_rule.ideal_batch
            num_batches = (remaining_quantity + batch_size - 1) // batch_size
            
            # Find available schedules
            for schedule in schedules.order_by('date'):
                available_capacity = schedule.mixer.mixer_max - schedule.capacity_reserved
                
                if available_capacity >= batch_size:
                    # Create batch assignment
                    actual_batch_size = min(batch_size, remaining_quantity)
                    assignment = BatchAssignment.objects.create(
                        batch_schedule=schedule,
                        production_order=order,
                        priority=order.priority,
                        quantity=actual_batch_size
                    )
                    optimized_assignments.append(assignment)
                    
                    remaining_quantity -= actual_batch_size
                    if remaining_quantity <= 0:
                        break
        
        serializer = self.get_serializer(optimized_assignments, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def daily_schedule(self, request):
        """Get detailed schedule for a specific date."""
        date = request.query_params.get('date', timezone.now().date().isoformat())
        mixer_id = request.query_params.get('mixer')
        
        assignments = self.get_queryset().filter(
            batch_schedule__date=date
        ).order_by(
            'batch_schedule__mixer',
            'sequence_number'
        )
        
        if mixer_id:
            assignments = assignments.filter(batch_schedule__mixer_id=mixer_id)
        
        schedule_data = {}
        for assignment in assignments:
            mixer_id = assignment.batch_schedule.mixer_id
            if mixer_id not in schedule_data:
                schedule_data[mixer_id] = {
                    'mixer': assignment.batch_schedule.mixer.mixer,
                    'total_capacity': assignment.batch_schedule.mixer.mixer_max,
                    'used_capacity': assignment.batch_schedule.capacity_reserved,
                    'batches': []
                }
            
            schedule_data[mixer_id]['batches'].append({
                'sequence': assignment.sequence_number,
                'product': assignment.production_order.product.product,
                'quantity': assignment.quantity,
                'status': assignment.status,
                'start_time': assignment.start_time,
                'completion_time': assignment.completion_time
            })
        
        return Response(schedule_data)