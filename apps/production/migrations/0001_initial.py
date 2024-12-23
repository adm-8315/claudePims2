# Generated by Django 4.2.17 on 2024-12-23 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('equipmentid', models.AutoField(db_column='equipmentID', primary_key=True, serialize=False)),
                ('equipment', models.CharField(blank=True, max_length=255, null=True)),
                ('identifier', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'equipment',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Equipmentstatus',
            fields=[
                ('equipmentstatusid', models.AutoField(db_column='equipmentStatusID', primary_key=True, serialize=False)),
                ('equipmentstatus', models.CharField(db_column='equipmentStatus', max_length=255)),
            ],
            options={
                'db_table': 'equipmentstatus',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Equipmenttype',
            fields=[
                ('equipmenttypeid', models.AutoField(db_column='equipmentTypeID', primary_key=True, serialize=False)),
                ('equipmenttype', models.CharField(db_column='equipmentType', max_length=255)),
            ],
            options={
                'db_table': 'equipmenttype',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Preventativemaintenancetype',
            fields=[
                ('preventativemaintenancetypeid', models.AutoField(db_column='preventativeMaintenanceTypeID', primary_key=True, serialize=False)),
                ('preventativemaintenancetype', models.CharField(blank=True, db_column='preventativeMaintenanceType', max_length=255, null=True)),
            ],
            options={
                'db_table': 'preventativemaintenancetype',
                'managed': False,
            },
        ),
    ]