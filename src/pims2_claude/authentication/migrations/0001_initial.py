from django.db import migrations, models
from django.contrib.auth.hashers import make_password

def generate_superuser(apps, schema_editor):
    User = apps.get_model('core', 'User')
    Person = apps.get_model('core', 'Person')
    Location = apps.get_model('core', 'Location')
    Company = apps.get_model('core', 'Company')

    # Create default location and company if needed
    default_location = Location.objects.create(location='Default Location')
    default_company = Company.objects.create(company='Default Company')

    # Create admin person
    admin_person = Person.objects.create(
        first_name='Admin',
        last_name='User'
    )

    # Create admin user
    User.objects.create(
        username='admin',
        password_hash=make_password('admin'),  # This should be changed immediately
        person=admin_person,
        default_location=default_location,
        default_owner=default_company,
        active=True
    )

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(generate_superuser),
    ]
