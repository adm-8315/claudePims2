import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from datetime import timedelta, time
from core.models.scheduling import BatchSchedule, BatchAssignment, MixingRule
from core.models.production import ProductionOrder

@pytest.fixture
def create_mixer(db):
    from core.models.production import Mixer
    return Mixer.objects.create(
        mixer='Test Mixer',
        mixer_max=1000,
        active=True
    )

@pytest.fixture
def create_mixing_rule(db, create_product, create_mixer):
    return MixingRule.objects.create(
        product=create_product,
        mixer=create_mixer,
        minimum_batch=100,
        maximum_batch=500,
        ideal_batch=300,
        mixing_time=30,
        cleanup_time=15
    )

@pytest.fixture
def create_batch_schedule(db, create_mixer):
    return BatchSchedule.objects.create(
        date=timezone.now().date(),
        mixer=create_mixer,
        capacity_reserved=0
    )

@pytest.fixture
def create_batch_assignment(db, create_batch_schedule, create_production_order):
    return BatchAssignment.objects.create(
        batch_schedule=create_batch_schedule,
        production_order=create_production_order,
        priority=2,
        status='scheduled',
        quantity=200,
        sequence_number=1
    )

@pytest.mark.django_db
class TestScheduling:
    def test_create_mixing_rule(self, authenticated_client, create_product, create_mixer):
        url = reverse('mixingrule-list')
        data = {
            'product': create_product.id,
            'mixer': create_mixer.id,
            'minimum_batch': 100,
            'maximum_batch': 500,
            'ideal_batch': 300,
            'mixing_time': 30,
            'cleanup_time': 15
        }
        
        response = authenticated_client.post(url, data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['minimum_batch'] == 100
        assert response.data['maximum_batch'] == 500

    def test_create_batch_schedule(self, authenticated_client, create_mixer):
        url = reverse('batchschedule-list')
        data = {
            'date': timezone.now().date().isoformat(),
            'mixer': create_mixer.id,
            'notes': 'Test schedule'
        }
        
        response = authenticated_client.post(url, data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['capacity_reserved'] == 0

    def test_create_batch_assignment(self, authenticated_client, create_batch_schedule,
                                   create_production_order, create_mixing_rule):
        url = reverse('batchassignment-list')
        data = {
            'batch_schedule': create_batch_schedule.id,
            'production_order': create_production_order.id,
            'priority': 2,
            'quantity': 200
        }
        
        response = authenticated_client.post(url, data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['status'] == 'scheduled'
        assert response.data['sequence_number'] == 1

    def test_update_batch_status(self, authenticated_client, create_batch_assignment):
        url = reverse('batchassignment-update-status', kwargs={'pk': create_batch_assignment.id})
        data = {'status': 'in_progress'}
        
        response = authenticated_client.post(url, data)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'in_progress'
        assert response.data['start_time'] is not None

    def test_complete_batch(self, authenticated_client, create_batch_assignment):
        url = reverse('batchassignment-update-status', kwargs={'pk': create_batch_assignment.id})
        data = {'status': 'completed'}
        
        response = authenticated_client.post(url, data)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'completed'
        assert response.data['completion_time'] is not None

        # Verify production order was updated
        production_order = create_batch_assignment.production_order
        production_order.refresh_from_db()
        assert production_order.quantity_filled == create_batch_assignment.quantity

    def test_optimize_schedule(self, authenticated_client, create_mixer,
                             create_mixing_rule, create_production_order):
        # Create batch schedule for next 5 days
        today = timezone.now().date()
        for i in range(5):
            BatchSchedule.objects.create(
                date=today + timedelta(days=i),
                mixer=create_mixer,
                capacity_reserved=0
            )
        
        url = reverse('batchassignment-optimize-schedule')
        data = {
            'start_date': today.isoformat(),
            'end_date': (today + timedelta(days=4)).isoformat(),
            'mixer': create_mixer.id
        }
        
        response = authenticated_client.post(url, data)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) > 0  # Should have created some assignments

    def test_daily_schedule(self, authenticated_client, create_batch_assignment):
        url = reverse('batchassignment-daily-schedule')
        params = {'date': create_batch_assignment.batch_schedule.date.isoformat()}
        
        response = authenticated_client.get(url, params)
        
        assert response.status_code == status.HTTP_200_OK
        assert str(create_batch_assignment.batch_schedule.mixer.id) in response.data
        mixer_schedule = response.data[str(create_batch_assignment.batch_schedule.mixer.id)]
        assert len(mixer_schedule['batches']) == 1