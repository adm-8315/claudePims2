from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType

class Address(models.Model):
    addressid = models.AutoField(db_column='addressID', primary_key=True)
    lineone = models.CharField(db_column='lineOne', max_length=255)
    linetwo = models.CharField(db_column='lineTwo', max_length=255, blank=True, null=True)
    linethree = models.CharField(db_column='lineThree', max_length=255, blank=True, null=True)
    city = models.ForeignKey('City', models.DO_NOTHING, db_column='city')
    zip = models.CharField(max_length=6)
    state = models.ForeignKey('State', models.DO_NOTHING, db_column='state')

    class Meta:
        managed = False
        db_table = 'address'

class Preventativemaintenance(models.Model):
    preventativemaintenanceid = models.AutoField(db_column='preventativeMaintenanceID', primary_key=True)
    equipment = models.ForeignKey('production.Equipment', models.DO_NOTHING, db_column='equipment')
    preventativemaintenancetype = models.ForeignKey('production.Preventativemaintenancetype', models.DO_NOTHING, db_column='preventativeMaintenanceType', blank=True, null=True)
    preventativemaintenance = models.CharField(db_column='preventativeMaintenance', max_length=255, blank=True, null=True)
    valueint = models.PositiveIntegerField(db_column='valueInt', blank=True, null=True)
    valuedate = models.DateField(db_column='valueDate', blank=True, null=True)
    completedate = models.DateField(db_column='completeDate', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'preventativemaintenance'
