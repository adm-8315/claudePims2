from django.db import models

class Equipment(models.Model):
    equipmentid = models.AutoField(db_column='equipmentID', primary_key=True)
    equipment = models.CharField(max_length=255, blank=True, null=True)
    identifier = models.CharField(max_length=255, blank=True, null=True)
    equipmenttype = models.ForeignKey('Equipmenttype', models.DO_NOTHING, db_column='equipmentType')
    equipmentstatus = models.ForeignKey('Equipmentstatus', models.DO_NOTHING, db_column='equipmentStatus')
    location = models.ForeignKey('core.Location', models.DO_NOTHING, db_column='location')

    class Meta:
        managed = False
        db_table = 'equipment'

class Equipmentstatus(models.Model):
    equipmentstatusid = models.AutoField(db_column='equipmentStatusID', primary_key=True)
    equipmentstatus = models.CharField(db_column='equipmentStatus', max_length=255)

    class Meta:
        managed = False
        db_table = 'equipmentstatus'

class Equipmenttype(models.Model):
    equipmenttypeid = models.AutoField(db_column='equipmentTypeID', primary_key=True)
    equipmenttype = models.CharField(db_column='equipmentType', max_length=255)

    class Meta:
        managed = False
        db_table = 'equipmenttype'

class Preventativemaintenancetype(models.Model):
    preventativemaintenancetypeid = models.AutoField(db_column='preventativeMaintenanceTypeID', primary_key=True)
    preventativemaintenancetype = models.CharField(db_column='preventativeMaintenanceType', max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'preventativemaintenancetype'

# [Other production-related models...]