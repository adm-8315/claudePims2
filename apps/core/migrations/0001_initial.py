# Generated by Django 4.2.17 on 2024-12-23 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('addressid', models.AutoField(db_column='addressID', primary_key=True, serialize=False)),
                ('lineone', models.CharField(db_column='lineOne', max_length=255)),
                ('linetwo', models.CharField(blank=True, db_column='lineTwo', max_length=255, null=True)),
                ('linethree', models.CharField(blank=True, db_column='lineThree', max_length=255, null=True)),
                ('zip', models.CharField(max_length=6)),
            ],
            options={
                'db_table': 'address',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('cityid', models.AutoField(db_column='cityID', primary_key=True, serialize=False)),
                ('city', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'city',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('locationid', models.AutoField(db_column='locationID', primary_key=True, serialize=False)),
                ('location', models.CharField(max_length=255)),
                ('active', models.IntegerField()),
            ],
            options={
                'db_table': 'location',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('stateid', models.AutoField(db_column='stateID', primary_key=True, serialize=False)),
                ('state', models.CharField(max_length=255)),
                ('abbreviation', models.CharField(max_length=2)),
            ],
            options={
                'db_table': 'state',
                'managed': False,
            },
        ),
    ]