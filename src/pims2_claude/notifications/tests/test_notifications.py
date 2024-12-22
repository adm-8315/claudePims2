import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from notifications.models import (
    Notification,
    NotificationTemplate,
    NotificationPreference
)
from notifications.services import NotificationService

@pytest.fixture
def create_notification_template(db):
    return NotificationTemplate.objects.create(
        name='test_template',
        subject='Test Notification',
        body='Hello {{ name }}! This is a test notification.'
    )

@pytest.fixture
def create_notification(db, create_user):
    return Notification.objects.create(
        recipient=create_user().person,
        subject='Test Notification',
        message='This is a test notification',
        priority='medium'
    )

@pytest.fixture
def create_notification_preference(db, create_user):
    return NotificationPreference.objects.create(
        person=create_user().person,
        event_type='batch_completed',
        email_enabled=True,
        push_enabled=True,
        minimum_priority='low'
    )

@pytest.mark.django_db
class TestNotifications:
    def test_create_notification(self, authenticated_client, create_user):
        url = reverse('notification-list')
        data = {
            'recipient': create_user().person.id,
            'subject': 'Test Notification',
            'message': 'This is a test notification',
            'priority': 'medium'
        }

        response = authenticated_client.post(url, data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['subject'] == 'Test Notification'

    def test_mark_notification_read(self, authenticated_client, create_notification):
        url = reverse('notification-mark-read', kwargs={'pk': create_notification.id})

        response = authenticated_client.post(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['read'] is True
        assert response.data['read_at'] is not None

    def test_get_unread_count(self, authenticated_client, create_notification):
        url = reverse('notification-unread-count')

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['unread_count'] == 1

    def test_render_template(self, create_notification_template):
        context = {'name': 'John'}
        rendered = NotificationService.render_template(
            'test_template',
            context
        )

        assert rendered is not None
        assert rendered['subject'] == 'Test Notification'
        assert 'Hello John!' in rendered['message']

    def test_update_notification_preferences(self, authenticated_client, create_notification_preference):
        url = reverse('notificationpreference-detail', 
                     kwargs={'pk': create_notification_preference.id})
        data = {
            'email_enabled': False,
            'push_enabled': True,
            'minimum_priority': 'medium'
        }

        response = authenticated_client.patch(url, data)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['email_enabled'] is False
        assert response.data['minimum_priority'] == 'medium'

    def test_bulk_update_preferences(self, authenticated_client, create_user):
        url = reverse('notificationpreference-bulk-update')
        data = {
            'preferences': [
                {
                    'event_type': 'batch_completed',
                    'email_enabled': True,
                    'push_enabled': False,
                    'minimum_priority': 'high'
                },
                {
                    'event_type': 'low_stock',
                    'email_enabled': True,
                    'push_enabled': True,
                    'minimum_priority': 'urgent'
                }
            ]
        }

        response = authenticated_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_get_available_events(self, authenticated_client):
        url = reverse('notificationpreference-available-events')

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert 'batch_completed' in response.data['events']
        assert 'low_stock' in response.data['events']