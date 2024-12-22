from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.db import transaction

from core.models.scheduling import BatchAssignment
from core.models.product import ProductInventory
from core.models.production import ProductionOrder
from .services import NotificationService

@receiver(post_save, sender=BatchAssignment)
def handle_batch_status_change(sender, instance, created, **kwargs):
    """Send notifications when batch status changes."""
    if not created and instance.tracker.has_changed('status'):
        if instance.status == 'completed':
            # Notify production manager
            production_manager = instance.production_order.user.person
            template_data = {
                'batch_id': instance.id,
                'product': instance.production_order.product.product,
                'quantity': instance.quantity,
                'completion_time': instance.completion_time
            }
            rendered = NotificationService.render_template(
                'batch_completed',
                template_data
            )
            if rendered:
                NotificationService.create_notification(
                    recipient=production_manager,
                    subject=rendered['subject'],
                    message=rendered['message'],
                    priority='medium',
                    event_type='batch_completed'
                )

@receiver(post_save, sender=ProductInventory)
def handle_low_stock(sender, instance, **kwargs):
    """Send notifications for low stock levels."""
    if instance.stock <= instance.stock_level_warning:
        # Get inventory managers
        inventory_managers = instance.companyLocationLink.location.userLocationLink_set.all()
        template_data = {
            'product': instance.product.product,
            'current_stock': instance.stock,
            'warning_level': instance.stock_level_warning,
            'location': instance.companyLocationLink.location.location
        }
        rendered = NotificationService.render_template(
            'low_stock',
            template_data
        )
        if rendered:
            for user_location in inventory_managers:
                NotificationService.create_notification(
                    recipient=user_location.user.person,
                    subject=rendered['subject'],
                    message=rendered['message'],
                    priority='high',
                    event_type='low_stock'
                )

@receiver(post_save, sender=ProductionOrder)
def handle_order_completion(sender, instance, created, **kwargs):
    """Send notifications when production orders are completed."""
    if not created and instance.tracker.has_changed('active'):
        if not instance.active and instance.quantity_filled >= instance.quantity_ordered:
            template_data = {
                'order_id': instance.id,
                'product': instance.product.product,
                'quantity': instance.quantity_ordered,
                'completion_date': instance.fill_date
            }
            rendered = NotificationService.render_template(
                'order_completed',
                template_data
            )
            if rendered:
                NotificationService.create_notification(
                    recipient=instance.user.person,
                    subject=rendered['subject'],
                    message=rendered['message'],
                    priority='medium',
                    event_type='order_completed'
                )