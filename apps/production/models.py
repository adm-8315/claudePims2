from django.db import models
from django.conf import settings

class Equipment(models.Model):
    equipmentid = models.AutoField(db_column='equipmentID', primary_key=True)
    equipment = models.CharField(max_length=255, blank=True, null=True)
    identifier = models.CharField(max_length=255, blank=True, null=True)
    equipmenttype = models.ForeignKey('EquipmentType', models.CASCADE, db_column='equipmentType')
    equipmentstatus = models.ForeignKey('EquipmentStatus', models.CASCADE, db_column='equipmentStatus')
    location = models.ForeignKey('core.Location', models.CASCADE, db_column='location')

    class Meta:
        db_table = 'equipment'

class EquipmentType(models.Model):
    equipmenttypeid = models.AutoField(db_column='equipmentTypeID', primary_key=True)
    equipmenttype = models.CharField(db_column='equipmentType', max_length=255)

    class Meta:
        db_table = 'equipmenttype'

class EquipmentStatus(models.Model):
    equipmentstatusid = models.AutoField(db_column='equipmentStatusID', primary_key=True)
    equipmentstatus = models.CharField(db_column='equipmentStatus', max_length=255)

    class Meta:
        db_table = 'equipmentstatus'

class PreventativeMaintenanceType(models.Model):
    preventativemaintenancetypeid = models.AutoField(db_column='preventativeMaintenanceTypeID', primary_key=True)
    preventativemaintenancetype = models.CharField(db_column='preventativeMaintenanceType', max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'preventativemaintenancetype'

class PreventativeMaintenance(models.Model):
    preventativemaintenanceid = models.AutoField(db_column='preventativeMaintenanceID', primary_key=True)
    equipment = models.ForeignKey(Equipment, models.CASCADE, db_column='equipment')
    preventativemaintenancetype = models.ForeignKey(PreventativeMaintenanceType, models.SET_NULL, db_column='preventativeMaintenanceType', blank=True, null=True)
    preventativemaintenance = models.CharField(db_column='preventativeMaintenance', max_length=255, blank=True, null=True)
    valueint = models.PositiveIntegerField(db_column='valueInt', blank=True, null=True)
    valuedate = models.DateField(db_column='valueDate', blank=True, null=True)
    completedate = models.DateField(db_column='completeDate', blank=True, null=True)

    class Meta:
        db_table = 'preventativemaintenance'

class PreventativeMaintenanceLog(models.Model):
    preventativemaintenancelogid = models.AutoField(db_column='preventativeMaintenanceLogID', primary_key=True)
    equipment = models.ForeignKey(Equipment, models.CASCADE, db_column='equipment')
    preventativemaintenancetype = models.ForeignKey(PreventativeMaintenanceType, models.CASCADE, db_column='preventativeMaintenanceType')
    completedate = models.DateField(db_column='completeDate')
    notes = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'preventativemaintenancelog'

class Job(models.Model):
    jobid = models.AutoField(db_column='jobID', primary_key=True)
    job = models.CharField(max_length=255)
    companylocationlink = models.ForeignKey('core.CompanyLocationLink', models.CASCADE, db_column='companyLocationLink')
    startdate = models.DateField(db_column='startDate', blank=True, null=True)
    enddate = models.DateField(db_column='endDate', blank=True, null=True)

    class Meta:
        db_table = 'job'

class EquipmentList(models.Model):
    equipmentlistid = models.AutoField(db_column='equipmentListID', primary_key=True)
    equipment = models.ForeignKey(Equipment, models.CASCADE, db_column='equipment')
    job = models.ForeignKey(Job, models.CASCADE, db_column='job')

    class Meta:
        db_table = 'equipmentlist'
        unique_together = (('equipment', 'job'),)

class Form(models.Model):
    formid = models.AutoField(db_column='formID', primary_key=True)
    formtag = models.CharField(db_column='formTag', max_length=4, blank=True, null=True)
    formlocation = models.CharField(db_column='formLocation', max_length=255, blank=True, null=True)
    formquantity = models.IntegerField(db_column='formQuantity')
    formpieces = models.IntegerField(db_column='formPieces')
    notes = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'form'

class FormProductLink(models.Model):
    form = models.ForeignKey(Form, models.CASCADE, db_column='form')
    product = models.ForeignKey('inventory.Product', models.CASCADE, db_column='product')

    class Meta:
        db_table = 'formproductlink'
        unique_together = (('form', 'product'),)

class Furnace(models.Model):
    furnaceid = models.AutoField(db_column='furnaceID', primary_key=True)
    furnace = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'furnace'

class FurnacePattern(models.Model):
    furnacepatternid = models.AutoField(db_column='furnacePatternID', primary_key=True)
    furnace = models.ForeignKey(Furnace, models.CASCADE, db_column='furnace')
    furnacepattern = models.CharField(db_column='furnacePattern', max_length=255)
    patterndescription = models.CharField(db_column='patternDescription', max_length=255, blank=True, null=True)
    patterntemperature = models.IntegerField(db_column='patternTemperature', blank=True, null=True)
    patterntime = models.IntegerField(db_column='patternTime', blank=True, null=True)

    class Meta:
        db_table = 'furnacepattern'

class ProductionOrder(models.Model):
    productionorderid = models.AutoField(db_column='productionOrderID', primary_key=True)
    product = models.ForeignKey('inventory.Product', models.CASCADE, db_column='product')
    quantityordered = models.IntegerField(db_column='quantityOrdered', blank=True, null=True)
    quantityfilled = models.IntegerField(db_column='quantityFilled', blank=True, null=True)
    filldate = models.DateField(db_column='fillDate', blank=True, null=True)
    notes = models.CharField(max_length=255, blank=True, null=True)
    form = models.ForeignKey(Form, models.SET_NULL, db_column='form', blank=True, null=True)
    taps = models.IntegerField(blank=True, null=True)
    lowerspec = models.FloatField(db_column='lowerSpec', blank=True, null=True)
    upperspec = models.FloatField(db_column='upperSpec', blank=True, null=True)
    furnacepattern = models.ForeignKey(FurnacePattern, models.SET_NULL, db_column='furnacePattern', blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, db_column='user')
    lastedit = models.DateTimeField(db_column='lastEdit')
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'productionorder'

class ProductionOrderSchedule(models.Model):
    productionorderscheduleid = models.AutoField(db_column='productionOrderScheduleID', primary_key=True)
    productionorder = models.ForeignKey(ProductionOrder, models.CASCADE, db_column='productionOrder')
    pourdate = models.DateField(db_column='pourDate')
    stripdate = models.DateField(db_column='stripDate')
    firedate = models.DateField(db_column='fireDate')
    quantity = models.IntegerField()
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'productionorderschedule'
        unique_together = (('pourdate', 'productionorder'),)

class ProductionOrderScheduleBatching(models.Model):
    productionorderschedulebatchingid = models.AutoField(db_column='productionOrderScheduleBatchingID', primary_key=True)
    productionorderschedule = models.ForeignKey(ProductionOrderSchedule, models.CASCADE, db_column='productionOrderSchedule')
    batchnumber = models.IntegerField(db_column='batchNumber')
    quantity = models.IntegerField()

    class Meta:
        db_table = 'productionorderschedulebatching'

class QCTest(models.Model):
    qctestid = models.AutoField(db_column='qcTestID', primary_key=True)
    material = models.ForeignKey('inventory.Material', models.CASCADE, db_column='material')
    qctest = models.CharField(db_column='qcTest', max_length=255)
    lowerspec = models.FloatField(db_column='lowerSpec', blank=True, null=True)
    upperspec = models.FloatField(db_column='upperSpec', blank=True, null=True)
    target = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'qctest'

class QCTestData(models.Model):
    qctestdataid = models.AutoField(db_column='qcTestDataID', primary_key=True)
    qctest = models.ForeignKey(QCTest, models.CASCADE, db_column='qcTest')
    value = models.FloatField()
    testdate = models.DateTimeField(db_column='testDate', auto_now_add=True)
    notes = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'qctestdata'
