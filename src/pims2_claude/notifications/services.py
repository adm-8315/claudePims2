from django.core.mail import send_mail
from django.conf import settings
from django.template import Template, Context
from django.utils import timezone

from .models import Notification, NotificationTemplate, NotificationPreference

class NotificationService:
    @staticmethod
    def create_notification(recipient, subject, message, priority='medium', event_type=None):
        """Create a notification and send it based on user preferences."""
        # Check notification preferences if event_type is provided
        if event_type:
            try:
                pref = NotificationPreference.objects.get(
                    person=recipient,
                    event_type=event_type
                )
                # Check if priority meets minimum threshold
                priority_levels = {'low': 0, 'medium': 1, 'high': 2, 'urgent': 3}
                if priority_levels[priority] < priority_levels[pref.minimum_priority]:
                    return None
            except NotificationPreference.DoesNotExist:
                # Use default preferences
                pass

        notification = Notification.objects.create(
            recipient=recipient,
            subject=subject,
            message=message,
            priority=priority
        )

        NotificationService.send_notification(notification)
        return notification

    @staticmethod
    def send_notification(notification):
        """Send notification through configured channels."""
        if not notification.sent:
            # Get recipient's preferences
            prefs = NotificationPreference.objects.filter(person=notification.recipient)
            
            # Send email if enabled
            email_enabled = True  # Default if no preference set
            email_pref = prefs.filter(email_enabled=True).exists()
            if email_enabled:
                NotificationService.send_email_notification(notification)

            # Update notification status
            notification.sent = True
            notification.sent_at = timezone.now()
            notification.save()

    @staticmethod
    def send_email_notification(notification):
        """Send notification via email."""
        # Get recipient's email
        recipient_email = notification.recipient.emails.filter(
            personemaillink__is_primary=True
        ).first()

        if recipient_email:
            try:
                send_mail(
                    subject=notification.subject,
                    message=notification.message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[recipient_email.full_email],
                    fail_silently=False
                )
            except Exception as e:
                # Log error but don't raise it
                print(f'Error sending email notification: {e}')

    @staticmethod
    def render_template(template_name, context_data):
        """Render notification template with given context."""
        try:
            template = NotificationTemplate.objects.get(name=template_name)
            t = Template(template.body)
            c = Context(context_data)
            return {
                'subject': template.subject,
                'message': t.render(c)
            }
        except NotificationTemplate.DoesNotExist:
            return None