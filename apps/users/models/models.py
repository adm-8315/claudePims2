from django.db import models

from apps.core.models import *

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


