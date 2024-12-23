from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone

from .models import Notification, NotificationTemplate, NotificationPreference
from .serializers import (
    NotificationSerializer,
    NotificationTemplateSerializer,
    NotificationPreferenceSerializer
)
from .services import NotificationService

class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Users can only see their own notifications
        return Notification.objects.filter(
            recipient=self.request.user.person
        ).order_by('-created_at')

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        notification = self.get_object()
        if not notification.read:
            notification.read = True
            notification.read_at = timezone.now()
            notification.save()
        return Response(self.get_serializer(notification).data)

    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        self.get_queryset().filter(read=False).update(
            read=True,
            read_at=timezone.now()
        )
        return Response({'status': 'success'})

    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        count = self.get_queryset().filter(read=False).count()
        return Response({'unread_count': count})

class NotificationTemplateViewSet(viewsets.ModelViewSet):
    queryset = NotificationTemplate.objects.all()
    serializer_class = NotificationTemplateSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def preview(self, request, pk=None):
        template = self.get_object()
        context_data = request.data.get('context', {})
        try:
            rendered = NotificationService.render_template(
                template.name,
                context_data
            )
            return Response(rendered)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class NotificationPreferenceViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationPreferenceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Users can only see and edit their own preferences
        return NotificationPreference.objects.filter(
            person=self.request.user.person
        )

    def perform_create(self, serializer):
        serializer.save(person=self.request.user.person)

    @action(detail=False, methods=['get'])
    def available_events(self, request):
        """List all available notification event types."""
        return Response({
            'events': dict(NotificationPreference.EVENT_CHOICES)
        })

    @action(detail=False, methods=['post'])
    def bulk_update(self, request):
        """Update multiple preferences at once."""
        preferences = request.data.get('preferences', [])
        updated = []

        for pref in preferences:
            instance, created = NotificationPreference.objects.update_or_create(
                person=self.request.user.person,
                event_type=pref['event_type'],
                defaults={
                    'email_enabled': pref.get('email_enabled', True),
                    'push_enabled': pref.get('push_enabled', True),
                    'minimum_priority': pref.get('minimum_priority', 'low')
                }
            )
            updated.append(self.get_serializer(instance).data)

        return Response(updated)