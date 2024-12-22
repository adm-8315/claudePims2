from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

class BatchSchedule(models.Model):
    date = models.DateField()
    mixer = models.ForeignKey('Mixer', on_delete=models.PROTECT)
    capacity_reserved = models.IntegerField(default=0)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['date', 'mixer']
        ordering = ['date', 'mixer']

    def __str__(self):
        return f'{self.date} - {self.mixer}'

    def validate_capacity(self):
        if self.capacity_reserved > self.mixer.mixer_max:
            raise ValidationError(f'Capacity exceeds mixer maximum of {self.mixer.mixer_max}')

    def save(self, *args, **kwargs):
        self.validate_capacity()
        super().save(*args, **kwargs)

class BatchAssignment(models.Model):
    PRIORITY_CHOICES = [
        (1, 'Low'),
        (2, 'Normal'),
        (3, 'High'),
        (4, 'Urgent')
    ]

    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ]

    batch_schedule = models.ForeignKey(BatchSchedule, on_delete=models.CASCADE)
    production_order = models.ForeignKey('ProductionOrder', on_delete=models.CASCADE)
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    quantity = models.IntegerField()
    sequence_number = models.IntegerField()
    start_time = models.TimeField(null=True, blank=True)
    completion_time = models.TimeField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['batch_schedule', 'sequence_number']
        unique_together = ['batch_schedule', 'sequence_number']

    def __str__(self):
        return f'Batch {self.sequence_number} - {self.production_order}'

    def save(self, *args, **kwargs):
        if not self.sequence_number:
            # Auto-assign sequence number if not provided
            last_sequence = BatchAssignment.objects.filter(
                batch_schedule=self.batch_schedule
            ).order_by('-sequence_number').first()
            self.sequence_number = (last_sequence.sequence_number + 1 if last_sequence else 1)
        
        # Update batch schedule capacity
        current_capacity = self.batch_schedule.capacity_reserved
        if self.pk:  # If updating existing assignment
            old_assignment = BatchAssignment.objects.get(pk=self.pk)
            current_capacity -= old_assignment.quantity
        
        new_capacity = current_capacity + self.quantity
        if new_capacity > self.batch_schedule.mixer.mixer_max:
            raise ValidationError('Assignment would exceed mixer capacity')
        
        self.batch_schedule.capacity_reserved = new_capacity
        self.batch_schedule.save()
        
        super().save(*args, **kwargs)

class MixingRule(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    mixer = models.ForeignKey('Mixer', on_delete=models.CASCADE)
    minimum_batch = models.IntegerField()
    maximum_batch = models.IntegerField()
    ideal_batch = models.IntegerField()
    mixing_time = models.IntegerField(help_text='Time in minutes')
    cleanup_time = models.IntegerField(help_text='Time in minutes')
    notes = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = ['product', 'mixer']

    def __str__(self):
        return f'{self.product} - {self.mixer}'

    def clean(self):
        if self.minimum_batch > self.maximum_batch:
            raise ValidationError('Minimum batch size cannot be greater than maximum')
        if self.ideal_batch < self.minimum_batch or self.ideal_batch > self.maximum_batch:
            raise ValidationError('Ideal batch size must be between minimum and maximum')
