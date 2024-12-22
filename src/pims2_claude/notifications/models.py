from django.db import models
from django.conf import settings

class NotificationTemplate(models.Model):
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=200)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Notification(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent')
    ]

    recipient = models.ForeignKey('core.Person', on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    sent = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, blank=True)
    read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.subject} - {self.recipient}'

class NotificationPreference(models.Model):
    EVENT_CHOICES = [
        ('batch_completed', 'Batch Completed'),
        ('low_stock', 'Low Stock Alert'),
        ('schedule_created', 'Schedule Created'),
        ('order_completed', 'Order Completed'),
        ('quality_issue', 'Quality Issue')
    ]

    person = models.ForeignKey('core.Person', on_delete=models.CASCADE)
    event_type = models.CharField(max_length=50, choices=EVENT_CHOICES)
    email_enabled = models.BooleanField(default=True)
    push_enabled = models.BooleanField(default=True)
    minimum_priority = models.CharField(
        max_length=10,
        choices=Notification.PRIORITY_CHOICES,
        default='low'
    )

    class Meta:
        unique_together = ['person', 'event_type']

    def __str__(self):
        return f'{self.person} - {self.event_type}'