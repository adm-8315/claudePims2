# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Additive(models.Model):
    material = models.ForeignKey('Material', models.DO_NOTHING, db_column='material')
    std = models.FloatField(blank=True, null=True)
    lowerspec = models.FloatField(db_column='lowerSpec', blank=True, null=True)  # Field name made lowercase.
    upperspec = models.FloatField(db_column='upperSpec', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'additive'


class Address(models.Model):
    addressid = models.AutoField(db_column='addressID', primary_key=True)  # Field name made lowercase.
    lineone = models.CharField(db_column='lineOne', max_length=255)  # Field name made lowercase.
    linetwo = models.CharField(db_column='lineTwo', max_length=255, blank=True, null=True)  # Field name made lowercase.
    linethree = models.CharField(db_column='lineThree', max_length=255, blank=True, null=True)  # Field name made lowercase.
    city = models.ForeignKey('City', models.DO_NOTHING, db_column='city')
    zip = models.CharField(max_length=6)
    state = models.ForeignKey('State', models.DO_NOTHING, db_column='state')

    class Meta:
        managed = False
        db_table = 'address'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class City(models.Model):
    cityid = models.AutoField(db_column='cityID', primary_key=True)  # Field name made lowercase.
    city = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'city'


class Company(models.Model):
    companyid = models.AutoField(db_column='companyID', primary_key=True)  # Field name made lowercase.
    company = models.CharField(max_length=255)
    active = models.IntegerField()
    defaultperson = models.ForeignKey('Person', models.DO_NOTHING, db_column='defaultPerson', blank=True, null=True)  # Field name made lowercase.
    defaultnumber_phone = models.ForeignKey('Number', models.DO_NOTHING, db_column='defaultNumber_phone', blank=True, null=True)  # Field name made lowercase.
    defaultnumber_fax = models.ForeignKey('Number', models.DO_NOTHING, db_column='defaultNumber_fax', related_name='company_defaultnumber_fax_set', blank=True, null=True)  # Field name made lowercase.
    searchcount = models.IntegerField(db_column='searchCount')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'company'


class Companycompanypropertylink(models.Model):
    company = models.ForeignKey(Company, models.DO_NOTHING, db_column='company')
    companyproperty = models.ForeignKey('Companyproperty', models.DO_NOTHING, db_column='companyProperty')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'companycompanypropertylink'


class Companycompanytypelink(models.Model):
    company = models.ForeignKey(Company, models.DO_NOTHING, db_column='company')
    companytype = models.ForeignKey('Companytype', models.DO_NOTHING, db_column='companyType')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'companycompanytypelink'


class Companyemaillink(models.Model):
    company = models.ForeignKey(Company, models.DO_NOTHING, db_column='company')
    email = models.ForeignKey('Email', models.DO_NOTHING, db_column='email')
    primary = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'companyemaillink'


class Companylocationlink(models.Model):
    companylocationlinkid = models.AutoField(db_column='companyLocationLinkID', primary_key=True)  # Field name made lowercase.
    company = models.ForeignKey(Company, models.DO_NOTHING, db_column='company', blank=True, null=True)
    location = models.ForeignKey('Location', models.DO_NOTHING, db_column='location')

    class Meta:
        managed = False
        db_table = 'companylocationlink'


class Companylocationlinknumberlink(models.Model):
    companylocationlink = models.ForeignKey(Companylocationlink, models.DO_NOTHING, db_column='companyLocationLink')  # Field name made lowercase.
    number = models.ForeignKey('Number', models.DO_NOTHING, db_column='number')

    class Meta:
        managed = False
        db_table = 'companylocationlinknumberlink'


class Companylocationlinkpersonlink(models.Model):
    companylocationlink = models.ForeignKey(Companylocationlink, models.DO_NOTHING, db_column='companyLocationLink')  # Field name made lowercase.
    person = models.ForeignKey('Person', models.DO_NOTHING, db_column='person')

    class Meta:
        managed = False
        db_table = 'companylocationlinkpersonlink'


class Companyproperty(models.Model):
    companypropertyid = models.AutoField(db_column='companyPropertyID', primary_key=True)  # Field name made lowercase.
    companyproperty = models.CharField(db_column='companyProperty', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'companyproperty'


class Companytype(models.Model):
    companytypeid = models.AutoField(db_column='companyTypeID', primary_key=True)  # Field name made lowercase.
    companytype = models.CharField(db_column='companyType', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'companytype'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Email(models.Model):
    emailid = models.AutoField(db_column='emailID', primary_key=True)  # Field name made lowercase.
    user = models.CharField(max_length=58)
    domain = models.CharField(max_length=58)
    tld = models.CharField(max_length=6)

    class Meta:
        managed = False
        db_table = 'email'


class Equipment(models.Model):
    equipmentid = models.AutoField(db_column='equipmentID', primary_key=True)  # Field name made lowercase.
    equipment = models.CharField(max_length=255, blank=True, null=True)
    identifier = models.CharField(max_length=255, blank=True, null=True)
    equipmenttype = models.ForeignKey('Equipmenttype', models.DO_NOTHING, db_column='equipmentType')  # Field name made lowercase.
    equipmentstatus = models.ForeignKey('Equipmentstatus', models.DO_NOTHING, db_column='equipmentStatus')  # Field name made lowercase.
    location = models.ForeignKey('Location', models.DO_NOTHING, db_column='location')

    class Meta:
        managed = False
        db_table = 'equipment'


class Equipmentlist(models.Model):
    job = models.ForeignKey('Job', models.DO_NOTHING, db_column='job')
    equipment = models.OneToOneField(Equipment, models.DO_NOTHING, db_column='equipment', primary_key=True)

    class Meta:
        managed = False
        db_table = 'equipmentlist'
        unique_together = (('job', 'equipment'),)


class Equipmentstatus(models.Model):
    equipmentstatusid = models.AutoField(db_column='equipmentStatusID', primary_key=True)  # Field name made lowercase.
    equipmentstatus = models.CharField(db_column='equipmentStatus', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'equipmentstatus'


class Equipmenttype(models.Model):
    equipmenttypeid = models.AutoField(db_column='equipmentTypeID', primary_key=True)  # Field name made lowercase.
    equipmenttype = models.CharField(db_column='equipmentType', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'equipmenttype'


class Form(models.Model):
    formid = models.AutoField(db_column='formID', primary_key=True)  # Field name made lowercase.
    formtag = models.CharField(db_column='formTag', max_length=4, blank=True, null=True)  # Field name made lowercase.
    formlocation = models.CharField(db_column='formLocation', max_length=255, blank=True, null=True)  # Field name made lowercase.
    formquantity = models.IntegerField(db_column='formQuantity')  # Field name made lowercase.
    formpieces = models.IntegerField(db_column='formPieces')  # Field name made lowercase.
    notes = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'form'


class Formproductlink(models.Model):
    form = models.ForeignKey(Form, models.DO_NOTHING, db_column='form')
    product = models.ForeignKey('Product', models.DO_NOTHING, db_column='product')

    class Meta:
        managed = False
        db_table = 'formproductlink'
        unique_together = (('product', 'form'),)


class Furnace(models.Model):
    furnaceid = models.AutoField(db_column='furnaceID', primary_key=True)  # Field name made lowercase.
    furnace = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'furnace'


class Furnacepattern(models.Model):
    furnacepatternid = models.AutoField(db_column='furnacePatternID', primary_key=True)  # Field name made lowercase.
    furnace = models.ForeignKey(Furnace, models.DO_NOTHING, db_column='furnace')
    furnacepattern = models.CharField(db_column='furnacePattern', max_length=255)  # Field name made lowercase.
    patterndescription = models.CharField(db_column='patternDescription', max_length=255, blank=True, null=True)  # Field name made lowercase.
    patterntemperature = models.IntegerField(db_column='patternTemperature', blank=True, null=True)  # Field name made lowercase.
    patterntime = models.IntegerField(db_column='patternTime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'furnacepattern'


class Grouping(models.Model):
    groupingid = models.AutoField(db_column='groupingID', primary_key=True)  # Field name made lowercase.
    grouping = models.CharField(max_length=255)
    location = models.ForeignKey('Location', models.DO_NOTHING, db_column='location')

    class Meta:
        managed = False
        db_table = 'grouping'


class Groupingequipmentlink(models.Model):
    grouping = models.AutoField()
    equipment = models.ForeignKey(Equipment, models.DO_NOTHING, db_column='equipment')

    class Meta:
        managed = False
        db_table = 'groupingequipmentlink'


class Groupingitemlink(models.Model):
    grouping = models.AutoField()
    item = models.ForeignKey('Item', models.DO_NOTHING, db_column='item')
    value = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'groupingitemlink'
        unique_together = (('grouping', 'item'),)


class Groupinglist(models.Model):
    job = models.AutoField(primary_key=True)  # The composite primary key (job, grouping) found, that is not supported. The first column is selected.
    grouping = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'groupinglist'
        unique_together = (('job', 'grouping'), ('job', 'grouping'),)


class Item(models.Model):
    itemid = models.AutoField(db_column='itemID', primary_key=True)  # Field name made lowercase.
    item = models.CharField(max_length=255, blank=True, null=True)
    itemtype = models.ForeignKey('Itemtype', models.DO_NOTHING, db_column='itemType')  # Field name made lowercase.
    lastprice = models.CharField(db_column='lastPrice', max_length=255, blank=True, null=True)  # Field name made lowercase.
    lastsupplier = models.CharField(db_column='lastSupplier', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'item'


class Iteminventory(models.Model):
    iteminventoryid = models.AutoField(db_column='itemInventoryID', primary_key=True)  # Field name made lowercase.
    item = models.ForeignKey(Item, models.DO_NOTHING, db_column='item')
    location = models.ForeignKey('Location', models.DO_NOTHING, db_column='location', blank=True, null=True)
    stock = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'iteminventory'
        unique_together = (('item', 'location'),)


class Itemlist(models.Model):
    job = models.ForeignKey('Job', models.DO_NOTHING, db_column='job')
    iteminventory = models.OneToOneField(Iteminventory, models.DO_NOTHING, db_column='itemInventory', primary_key=True)  # Field name made lowercase.
    value = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'itemlist'
        unique_together = (('job', 'iteminventory'),)


class Itemtype(models.Model):
    itemtypeid = models.AutoField(db_column='itemTypeID', primary_key=True)  # Field name made lowercase.
    itemtype = models.CharField(db_column='itemType', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'itemtype'


class Job(models.Model):
    jobid = models.AutoField(db_column='jobID', primary_key=True)  # Field name made lowercase.
    jobnumber = models.CharField(db_column='jobNumber', max_length=255)  # Field name made lowercase.
    companylocationlink = models.ForeignKey(Companylocationlink, models.DO_NOTHING, db_column='companyLocationLink')  # Field name made lowercase.
    description = models.CharField(max_length=512, blank=True, null=True)
    startdate = models.DateField(db_column='startDate', blank=True, null=True)  # Field name made lowercase.
    deliverdate = models.DateField(db_column='deliverDate', blank=True, null=True)  # Field name made lowercase.
    delivervia = models.CharField(db_column='deliverVIA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    active = models.TextField()  # This field type is a guess.
    post = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'job'


class Location(models.Model):
    locationid = models.AutoField(db_column='locationID', primary_key=True)  # Field name made lowercase.
    location = models.CharField(max_length=255)
    stockable = models.IntegerField()
    address = models.ForeignKey(Address, models.DO_NOTHING, db_column='address', blank=True, null=True)
    region = models.ForeignKey('Region', models.DO_NOTHING, db_column='region', blank=True, null=True)
    active = models.IntegerField()
    searchcount = models.IntegerField(db_column='searchCount')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'location'


class Locationrequirementlink(models.Model):
    location = models.ForeignKey(Location, models.DO_NOTHING, db_column='location')
    requirement = models.ForeignKey('Requirement', models.DO_NOTHING, db_column='requirement')

    class Meta:
        managed = False
        db_table = 'locationrequirementlink'


class Material(models.Model):
    materialid = models.AutoField(db_column='materialID', primary_key=True)  # Field name made lowercase.
    materialtype = models.ForeignKey('Materialtype', models.DO_NOTHING, db_column='materialType')  # Field name made lowercase.
    cost = models.DecimalField(max_digits=11, decimal_places=2)
    measure = models.ForeignKey('Measure', models.DO_NOTHING, db_column='measure')
    material = models.CharField(max_length=255)
    waterlow = models.FloatField(db_column='waterLow', blank=True, null=True)  # Field name made lowercase.
    waterhigh = models.FloatField(db_column='waterHigh', blank=True, null=True)  # Field name made lowercase.
    mixlow = models.IntegerField(db_column='mixLow', blank=True, null=True)  # Field name made lowercase.
    mixhigh = models.IntegerField(db_column='mixHigh', blank=True, null=True)  # Field name made lowercase.
    taps = models.IntegerField(blank=True, null=True)
    lowerspec = models.FloatField(db_column='lowerSpec', blank=True, null=True)  # Field name made lowercase.
    upperspec = models.FloatField(db_column='upperSpec', blank=True, null=True)  # Field name made lowercase.
    stdwater = models.FloatField(db_column='stdWater', blank=True, null=True)  # Field name made lowercase.
    stdmix = models.IntegerField(db_column='stdMix', blank=True, null=True)  # Field name made lowercase.
    searchcount = models.IntegerField(db_column='searchCount')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'material'


class Materialinventory(models.Model):
    materialinventoryid = models.AutoField(db_column='materialInventoryID', primary_key=True)  # Field name made lowercase.
    material = models.ForeignKey(Material, models.DO_NOTHING, db_column='material')
    companylocationlink = models.ForeignKey(Companylocationlink, models.DO_NOTHING, db_column='companyLocationLink', blank=True, null=True)  # Field name made lowercase.
    stock = models.PositiveIntegerField()
    inprogress = models.PositiveIntegerField(db_column='inProgress')  # Field name made lowercase.
    stocklevelwarning = models.PositiveIntegerField(db_column='stockLevelWarning')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'materialinventory'
        unique_together = (('material', 'companylocationlink'),)


class Materialmanufacturerlink(models.Model):
    material = models.ForeignKey(Material, models.DO_NOTHING, db_column='material', blank=True, null=True)
    company = models.ForeignKey(Company, models.DO_NOTHING, db_column='company', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'materialmanufacturerlink'


class Materialtransaction(models.Model):
    materialtransactionid = models.AutoField(db_column='materialTransactionID', primary_key=True)  # Field name made lowercase.
    materialinventory = models.ForeignKey(Materialinventory, models.DO_NOTHING, db_column='materialInventory')  # Field name made lowercase.
    transactiontype = models.ForeignKey('Transactiontype', models.DO_NOTHING, db_column='transactionType')  # Field name made lowercase.
    value = models.IntegerField()
    cost = models.FloatField(blank=True, null=True)
    companylocationlink = models.ForeignKey(Companylocationlink, models.DO_NOTHING, db_column='companyLocationLink', blank=True, null=True)  # Field name made lowercase.
    user = models.ForeignKey('User', models.DO_NOTHING, db_column='user')
    timestamp = models.DateField()
    notes = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'materialtransaction'


class Materialtype(models.Model):
    materialtypeid = models.AutoField(db_column='materialTypeID', primary_key=True)  # Field name made lowercase.
    materialtype = models.CharField(db_column='materialType', max_length=25)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'materialtype'


class Measure(models.Model):
    measureid = models.AutoField(db_column='measureID', primary_key=True)  # Field name made lowercase.
    measureplural = models.CharField(db_column='measurePlural', max_length=255)  # Field name made lowercase.
    measuresingular = models.CharField(db_column='measureSingular', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'measure'


class Mixer(models.Model):
    mixerid = models.AutoField(db_column='mixerID', primary_key=True)  # Field name made lowercase.
    mixer = models.CharField(max_length=255, blank=True, null=True)
    mixermax = models.IntegerField(db_column='mixerMax')  # Field name made lowercase.
    active = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'mixer'


class Number(models.Model):
    numberid = models.AutoField(db_column='numberID', primary_key=True)  # Field name made lowercase.
    numbertype = models.ForeignKey('Numbertype', models.DO_NOTHING, db_column='numberType')  # Field name made lowercase.
    number = models.CharField(max_length=10)
    ext = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'number'


class Numbertype(models.Model):
    numbertypeid = models.AutoField(db_column='numberTypeID', primary_key=True)  # Field name made lowercase.
    numbertype = models.CharField(db_column='numberType', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'numbertype'


class Permissionapplication(models.Model):
    permissionapplicationid = models.AutoField(db_column='permissionApplicationID', primary_key=True)  # Field name made lowercase.
    permissionapplication = models.CharField(db_column='permissionApplication', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'permissionapplication'


class Permissionblock(models.Model):
    permissionblockid = models.AutoField(db_column='permissionBlockID', primary_key=True)  # Field name made lowercase.
    permissiongroup = models.ForeignKey('Permissiongroup', models.DO_NOTHING, db_column='permissionGroup')  # Field name made lowercase.
    permissionblock = models.CharField(db_column='permissionBlock', max_length=255)  # Field name made lowercase.
    permissionblockdescription = models.CharField(db_column='permissionBlockDescription', max_length=255, blank=True, null=True)  # Field name made lowercase.
    active = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'permissionblock'


class Permissiongroup(models.Model):
    permissiongroupid = models.AutoField(db_column='permissionGroupID', primary_key=True)  # Field name made lowercase.
    permissiongroup = models.CharField(db_column='permissionGroup', max_length=255)  # Field name made lowercase.
    locationbased = models.IntegerField(db_column='locationBased')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'permissiongroup'


class Permissionlink(models.Model):
    user = models.PositiveIntegerField()
    permissionblock = models.ForeignKey(Permissionblock, models.DO_NOTHING, db_column='permissionBlock')  # Field name made lowercase.
    alllocation = models.IntegerField(db_column='allLocation')  # Field name made lowercase.
    location = models.ForeignKey(Location, models.DO_NOTHING, db_column='location', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'permissionlink'


class Person(models.Model):
    personid = models.AutoField(db_column='personID', primary_key=True)  # Field name made lowercase.
    firstname = models.CharField(db_column='firstName', max_length=70)  # Field name made lowercase.
    lastname = models.CharField(db_column='lastName', max_length=35)  # Field name made lowercase.
    address = models.ForeignKey(Address, models.DO_NOTHING, db_column='address', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'person'


class Personemaillink(models.Model):
    person = models.ForeignKey(Person, models.DO_NOTHING, db_column='person')
    email = models.ForeignKey(Email, models.DO_NOTHING, db_column='email')
    primary = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'personemaillink'


class Personnumberlink(models.Model):
    person = models.ForeignKey(Person, models.DO_NOTHING, db_column='person')
    number = models.ForeignKey(Number, models.DO_NOTHING, db_column='number')

    class Meta:
        managed = False
        db_table = 'personnumberlink'


class Preventativemaintenance(models.Model):
    preventativemaintenanceid = models.AutoField(db_column='preventativeMaintenanceID', primary_key=True)  # Field name made lowercase.
    equipment = models.ForeignKey(Equipment, models.DO_NOTHING, db_column='equipment')
    preventativemaintenancetype = models.ForeignKey('Preventativemaintenancetype', models.DO_NOTHING, db_column='preventativeMaintenanceType', blank=True, null=True)  # Field name made lowercase.
    preventativemaintenance = models.CharField(db_column='preventativeMaintenance', max_length=255, blank=True, null=True)  # Field name made lowercase.
    valueint = models.PositiveIntegerField(db_column='valueInt', blank=True, null=True)  # Field name made lowercase.
    valuedate = models.DateField(db_column='valueDate', blank=True, null=True)  # Field name made lowercase.
    completedate = models.DateField(db_column='completeDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'preventativemaintenance'


class Preventativemaintenancelog(models.Model):
    preventativemaintenancelogid = models.AutoField(db_column='preventativeMaintenanceLogID', primary_key=True)  # Field name made lowercase.
    equipment = models.ForeignKey(Equipment, models.DO_NOTHING, db_column='equipment')
    preventativemaintenancetype = models.ForeignKey('Preventativemaintenancetype', models.DO_NOTHING, db_column='preventativeMaintenanceType')  # Field name made lowercase.
    date = models.DateField(blank=True, null=True)
    value = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'preventativemaintenancelog'


class Preventativemaintenancetype(models.Model):
    preventativemaintenancetypeid = models.AutoField(db_column='preventativeMaintenanceTypeID', primary_key=True)  # Field name made lowercase.
    preventativemaintenancetype = models.CharField(db_column='preventativeMaintenanceType', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'preventativemaintenancetype'


class Product(models.Model):
    productid = models.AutoField(db_column='productID', primary_key=True)  # Field name made lowercase.
    producttype = models.ForeignKey('Producttype', models.DO_NOTHING, db_column='productType')  # Field name made lowercase.
    cost = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    measure = models.IntegerField(blank=True, null=True)
    product = models.CharField(max_length=255, blank=True, null=True)
    searchcount = models.IntegerField(db_column='searchCount')  # Field name made lowercase.
    active = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'product'


class Productconsumerlink(models.Model):
    product = models.OneToOneField(Product, models.DO_NOTHING, db_column='product', primary_key=True)  # The composite primary key (product, companyLocationLink) found, that is not supported. The first column is selected.
    companylocationlink = models.ForeignKey(Companylocationlink, models.DO_NOTHING, db_column='companyLocationLink')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'productconsumerlink'
        unique_together = (('product', 'companylocationlink'), ('companylocationlink', 'product'),)


class Productinventory(models.Model):
    productinventoryid = models.AutoField(db_column='productInventoryID', primary_key=True)  # Field name made lowercase.
    product = models.ForeignKey(Product, models.DO_NOTHING, db_column='product')
    companylocationlink = models.ForeignKey(Companylocationlink, models.DO_NOTHING, db_column='companyLocationLink', blank=True, null=True)  # Field name made lowercase.
    stock = models.PositiveIntegerField()
    inprogress = models.PositiveIntegerField(db_column='inProgress')  # Field name made lowercase.
    stocklevelwarning = models.PositiveIntegerField(db_column='stockLevelWarning')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'productinventory'
        unique_together = (('product', 'companylocationlink'),)


class Productionorder(models.Model):
    productionorderid = models.AutoField(db_column='productionOrderID', primary_key=True)  # Field name made lowercase.
    product = models.ForeignKey(Product, models.DO_NOTHING, db_column='product')
    quantityordered = models.IntegerField(db_column='quantityOrdered', blank=True, null=True)  # Field name made lowercase.
    quantityfilled = models.IntegerField(db_column='quantityFilled', blank=True, null=True)  # Field name made lowercase.
    filldate = models.DateField(db_column='fillDate', blank=True, null=True)  # Field name made lowercase.
    notes = models.CharField(max_length=255, blank=True, null=True)
    form = models.ForeignKey(Form, models.DO_NOTHING, db_column='form', blank=True, null=True)
    taps = models.IntegerField(blank=True, null=True)
    lowerspec = models.FloatField(db_column='lowerSpec', blank=True, null=True)  # Field name made lowercase.
    upperspec = models.FloatField(db_column='upperSpec', blank=True, null=True)  # Field name made lowercase.
    furnacepattern = models.ForeignKey(Furnacepattern, models.DO_NOTHING, db_column='furnacePattern', blank=True, null=True)  # Field name made lowercase.
    user = models.PositiveIntegerField()
    lastedit = models.DateTimeField(db_column='lastEdit')  # Field name made lowercase.
    active = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'productionorder'


class Productionordermateriallink(models.Model):
    productionorder = models.ForeignKey(Productionorder, models.DO_NOTHING, db_column='productionOrder')  # Field name made lowercase.
    material = models.ForeignKey(Material, models.DO_NOTHING, db_column='material')
    quantity = models.FloatField(blank=True, null=True)
    water = models.FloatField(blank=True, null=True)
    mixtime = models.IntegerField(db_column='mixTime', blank=True, null=True)  # Field name made lowercase.
    vibrationtype = models.ForeignKey('Vibrationtype', models.DO_NOTHING, db_column='vibrationType')  # Field name made lowercase.
    vibrationtime = models.IntegerField(db_column='vibrationTime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'productionordermateriallink'
        unique_together = (('material', 'productionorder'),)


class Productionorderoption(models.Model):
    productionorderoptionid = models.AutoField(db_column='productionOrderOptionID', primary_key=True)  # Field name made lowercase.
    productionorderoptiontype = models.ForeignKey('Productionorderoptiontype', models.DO_NOTHING, db_column='productionOrderOptionType')  # Field name made lowercase.
    productionorderoption = models.CharField(db_column='productionOrderOption', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'productionorderoption'


class Productionorderoptiontype(models.Model):
    productionorderoptiontypeid = models.AutoField(db_column='productionOrderOptionTypeID', primary_key=True)  # Field name made lowercase.
    productionorderoptiontype = models.CharField(db_column='productionOrderOptionType', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'productionorderoptiontype'


class Productionorderproductionorderoptionlink(models.Model):
    productionorder = models.ForeignKey(Productionorder, models.DO_NOTHING, db_column='productionOrder')  # Field name made lowercase.
    productionorderoption = models.ForeignKey(Productionorderoption, models.DO_NOTHING, db_column='productionOrderOption')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'productionorderproductionorderoptionlink'
        unique_together = (('productionorder', 'productionorderoption'),)


class Productionorderschedule(models.Model):
    productionorder = models.ForeignKey(Productionorder, models.DO_NOTHING, db_column='productionOrder')  # Field name made lowercase.
    pourdate = models.DateField(db_column='pourDate', primary_key=True)  # Field name made lowercase. The composite primary key (pourDate, productionOrder) found, that is not supported. The first column is selected.
    stripdate = models.DateField(db_column='stripDate')  # Field name made lowercase.
    firedate = models.DateField(db_column='fireDate')  # Field name made lowercase.
    quantity = models.IntegerField()
    active = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'productionorderschedule'
        unique_together = (('pourdate', 'productionorder'), ('pourdate', 'productionorder'),)


class Productionorderschedulebatching(models.Model):
    pourdate = models.DateField(db_column='pourDate', primary_key=True)  # Field name made lowercase.
    batchingstring = models.TextField(db_column='batchingString', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'productionorderschedulebatching'


class Productionordertemplate(models.Model):
    productionordertemplateid = models.AutoField(db_column='productionOrderTemplateID', primary_key=True)  # Field name made lowercase.
    product = models.PositiveIntegerField()
    notes = models.CharField(max_length=255, blank=True, null=True)
    form = models.ForeignKey(Form, models.DO_NOTHING, db_column='form', blank=True, null=True)
    taps = models.IntegerField(blank=True, null=True)
    lowerspec = models.FloatField(db_column='lowerSpec', blank=True, null=True)  # Field name made lowercase.
    upperspec = models.FloatField(db_column='upperSpec', blank=True, null=True)  # Field name made lowercase.
    furnacepattern = models.ForeignKey(Furnacepattern, models.DO_NOTHING, db_column='furnacePattern', blank=True, null=True)  # Field name made lowercase.
    user = models.PositiveIntegerField()
    lastedit = models.DateTimeField(db_column='lastEdit')  # Field name made lowercase.
    active = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'productionordertemplate'


class Productionordertemplatemateriallink(models.Model):
    productionordertemplate = models.ForeignKey(Productionordertemplate, models.DO_NOTHING, db_column='productionOrderTemplate')  # Field name made lowercase.
    material = models.ForeignKey(Material, models.DO_NOTHING, db_column='material')
    quantity = models.FloatField(blank=True, null=True)
    water = models.FloatField(blank=True, null=True)
    mixtime = models.IntegerField(db_column='mixTime', blank=True, null=True)  # Field name made lowercase.
    vibrationtype = models.ForeignKey('Vibrationtype', models.DO_NOTHING, db_column='vibrationType')  # Field name made lowercase.
    vibrationtime = models.IntegerField(db_column='vibrationTime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'productionordertemplatemateriallink'
        unique_together = (('material', 'productionordertemplate'),)


class Productionordertemplateproductionorderoptionlink(models.Model):
    productionordertemplate = models.ForeignKey(Productionordertemplate, models.DO_NOTHING, db_column='productionOrderTemplate')  # Field name made lowercase.
    productionorderoption = models.ForeignKey(Productionorderoption, models.DO_NOTHING, db_column='productionOrderOption')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'productionordertemplateproductionorderoptionlink'
        unique_together = (('productionordertemplate', 'productionorderoption'),)


class Producttransaction(models.Model):
    producttransactionid = models.AutoField(db_column='productTransactionID', primary_key=True)  # Field name made lowercase.
    productinventory = models.ForeignKey(Productinventory, models.DO_NOTHING, db_column='productInventory')  # Field name made lowercase.
    transactiontype = models.ForeignKey('Transactiontype', models.DO_NOTHING, db_column='transactionType')  # Field name made lowercase.
    value = models.IntegerField()
    cost = models.FloatField(blank=True, null=True)
    companylocationlink = models.ForeignKey(Companylocationlink, models.DO_NOTHING, db_column='companyLocationLink', blank=True, null=True)  # Field name made lowercase.
    user = models.ForeignKey('User', models.DO_NOTHING, db_column='user')
    timestamp = models.DateField()
    notes = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'producttransaction'


class Producttype(models.Model):
    producttypeid = models.AutoField(db_column='productTypeID', primary_key=True)  # Field name made lowercase.
    producttype = models.CharField(db_column='productType', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'producttype'


class Qctest(models.Model):
    qctestid = models.AutoField(db_column='qcTestID', primary_key=True)  # Field name made lowercase.
    slot = models.IntegerField()
    starttime = models.DateTimeField(db_column='startTime')  # Field name made lowercase.
    stoptime = models.DateTimeField(db_column='stopTime', blank=True, null=True)  # Field name made lowercase.
    material = models.ForeignKey(Material, models.DO_NOTHING, db_column='material')
    water = models.FloatField()
    mix = models.IntegerField()
    vib = models.IntegerField()
    lotcode = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'qctest'


class Qctestdata(models.Model):
    qctest = models.PositiveIntegerField(db_column='qcTest', primary_key=True)  # Field name made lowercase. The composite primary key (qcTest, timestamp) found, that is not supported. The first column is selected.
    timestamp = models.DateTimeField()
    temperature = models.FloatField()

    class Meta:
        managed = False
        db_table = 'qctestdata'
        unique_together = (('qctest', 'timestamp'), ('qctest', 'timestamp'),)


class Region(models.Model):
    regionid = models.AutoField(db_column='regionID', primary_key=True)  # Field name made lowercase.
    region = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'region'


class Requirement(models.Model):
    requirementid = models.AutoField(db_column='requirementID', primary_key=True)  # Field name made lowercase.
    requirementtype = models.ForeignKey('Requirementtype', models.DO_NOTHING, db_column='requirementType')  # Field name made lowercase.
    requirement = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'requirement'


class Requirementtype(models.Model):
    requirementtypeid = models.AutoField(db_column='requirementTypeID', primary_key=True)  # Field name made lowercase.
    requirementtype = models.CharField(db_column='requirementType', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'requirementtype'


class State(models.Model):
    stateid = models.AutoField(db_column='stateID', primary_key=True)  # Field name made lowercase.
    state = models.CharField(max_length=255)
    short = models.CharField(max_length=2)

    class Meta:
        managed = False
        db_table = 'state'


class Transactiontype(models.Model):
    transactiontypeid = models.AutoField(db_column='transactionTypeID', primary_key=True)  # Field name made lowercase.
    transactiontype = models.CharField(db_column='transactionType', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'transactiontype'


class User(models.Model):
    userid = models.AutoField(db_column='userID', primary_key=True)  # Field name made lowercase.
    active = models.IntegerField()
    person = models.ForeignKey(Person, models.DO_NOTHING, db_column='person')
    username = models.CharField(max_length=255)
    passwordhash = models.CharField(db_column='passwordHash', max_length=40)  # Field name made lowercase.
    defaultlocation = models.ForeignKey(Location, models.DO_NOTHING, db_column='defaultLocation')  # Field name made lowercase.
    defaultowner = models.ForeignKey(Company, models.DO_NOTHING, db_column='defaultOwner')  # Field name made lowercase.
    lastupdate = models.DateTimeField(db_column='lastUpdate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'user'


class Userlocationlink(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING, db_column='user')
    location = models.ForeignKey(Location, models.DO_NOTHING, db_column='location')

    class Meta:
        managed = False
        db_table = 'userlocationlink'


class Vibrationtype(models.Model):
    vibrationtypeid = models.AutoField(db_column='vibrationTypeID', primary_key=True)  # Field name made lowercase.
    vibrationtype = models.CharField(db_column='vibrationType', max_length=7, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'vibrationtype'


class Website(models.Model):
    company = models.ForeignKey(Company, models.DO_NOTHING, db_column='company')
    website = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'website'
