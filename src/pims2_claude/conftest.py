import pytest
from rest_framework.test import APIClient
from core.models.users import User, Person
from core.models.company import Company, Location

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user(db):
    def make_user(username='testuser', password='testpass123'):
        location = Location.objects.create(location='Test Location')
        company = Company.objects.create(company='Test Company')
        person = Person.objects.create(
            first_name='Test',
            last_name='User'
        )
        user = User.objects.create(
            username=username,
            password_hash=password,  # In a real app, this would be hashed
            person=person,
            default_location=location,
            default_owner=company,
            active=True
        )
        return user
    return make_user

@pytest.fixture
def authenticated_client(api_client, create_user):
    user = create_user()
    api_client.force_authenticate(user=user)
    return api_client