from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(max_length=255)),
                ('short', models.CharField(max_length=2)),
            ],
            options={
                'db_table': 'state',
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'city',
                'verbose_name_plural': 'cities',
            },
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('line_one', models.CharField(max_length=255)),
                ('line_two', models.CharField(blank=True, max_length=255, null=True)),
                ('line_three', models.CharField(blank=True, max_length=255, null=True)),
                ('zip', models.CharField(max_length=6)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.city')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.state')),
            ],
            options={
                'db_table': 'address',
                'verbose_name_plural': 'addresses',
            },
        ),
        # Add more model migrations here as needed
    ]
