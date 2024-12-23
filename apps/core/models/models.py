from django.db import models
from django.conf import settings

class State(models.Model):
    stateid = models.AutoField(db_column='stateID', primary_key=True)
    state = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=2)

    class Meta:
        db_table = 'state'

class City(models.Model):
    cityid = models.AutoField(db_column='cityID', primary_key=True)
    city = models.CharField(max_length=255)

    class Meta:
        db_table = 'city'

class Region(models.Model):
    regionid = models.AutoField(db_column='regionID', primary_key=True)
    region = models.CharField(max_length=255)

    class Meta:
        db_table = 'region'

class Address(models.Model):
    addressid = models.AutoField(db_column='addressID', primary_key=True)
    lineone = models.CharField(db_column='lineOne', max_length=255)
    linetwo = models.CharField(db_column='lineTwo', max_length=255, blank=True, null=True)
    linethree = models.CharField(db_column='lineThree', max_length=255, blank=True, null=True)
    city = models.ForeignKey(City, models.DO_NOTHING, db_column='city')
    zip = models.CharField(max_length=6)
    state = models.ForeignKey(State, models.DO_NOTHING, db_column='state')

    class Meta:
        db_table = 'address'

class Person(models.Model):
    personid = models.AutoField(db_column='personID', primary_key=True)
    firstname = models.CharField(db_column='firstName', max_length=255)
    lastname = models.CharField(db_column='lastName', max_length=255)
    address = models.ForeignKey(Address, models.SET_NULL, db_column='address', null=True, blank=True)

    class Meta:
        db_table = 'person'

class Company(models.Model):
    companyid = models.AutoField(db_column='companyID', primary_key=True)
    company = models.CharField(max_length=255)
    defaultperson = models.ForeignKey(Person, models.SET_NULL, db_column='defaultPerson', null=True, blank=True)
    defaultnumber_phone = models.ForeignKey('Number', models.SET_NULL, db_column='defaultNumber_phone', related_name='company_phone', null=True, blank=True)
    defaultnumber_fax = models.ForeignKey('Number', models.SET_NULL, db_column='defaultNumber_fax', related_name='company_fax', null=True, blank=True)

    class Meta:
        db_table = 'company'

class Location(models.Model):
    locationid = models.AutoField(db_column='locationID', primary_key=True)
    location = models.CharField(max_length=255)
    address = models.ForeignKey(Address, models.SET_NULL, db_column='address', null=True, blank=True)
    region = models.ForeignKey(Region, models.SET_NULL, db_column='region', null=True, blank=True)

    class Meta:
        db_table = 'location'

class CompanyLocationType(models.Model):
    companytypeid = models.AutoField(db_column='companyTypeID', primary_key=True)
    companytype = models.CharField(db_column='companyType', max_length=255)

    class Meta:
        db_table = 'companytype'

class CompanyLocationLink(models.Model):
    companylocationlinkid = models.AutoField(db_column='companyLocationLinkID', primary_key=True)
    company = models.ForeignKey(Company, models.CASCADE, db_column='company')
    location = models.ForeignKey(Location, models.CASCADE, db_column='location')

    class Meta:
        db_table = 'companylocationlink'
        unique_together = (('company', 'location'),)

class Number(models.Model):
    numberid = models.AutoField(db_column='numberID', primary_key=True)
    number = models.CharField(max_length=255)
    numbertype = models.ForeignKey('NumberType', models.DO_NOTHING, db_column='numberType')

    class Meta:
        db_table = 'number'

class NumberType(models.Model):
    numbertypeid = models.AutoField(db_column='numberTypeID', primary_key=True)
    numbertype = models.CharField(db_column='numberType', max_length=255)

    class Meta:
        db_table = 'numbertype'

class Email(models.Model):
    emailid = models.AutoField(db_column='emailID', primary_key=True)
    email = models.EmailField(max_length=255)

    class Meta:
        db_table = 'email'

class CompanyEmailLink(models.Model):
    company = models.ForeignKey(Company, models.CASCADE, db_column='company')
    email = models.ForeignKey(Email, models.CASCADE, db_column='email')

    class Meta:
        db_table = 'companyemaillink'
        unique_together = (('company', 'email'),)

class PersonEmailLink(models.Model):
    person = models.ForeignKey(Person, models.CASCADE, db_column='person')
    email = models.ForeignKey(Email, models.CASCADE, db_column='email')

    class Meta:
        db_table = 'personemaillink'
        unique_together = (('person', 'email'),)

class PersonNumberLink(models.Model):
    person = models.ForeignKey(Person, models.CASCADE, db_column='person')
    number = models.ForeignKey(Number, models.CASCADE, db_column='number')

    class Meta:
        db_table = 'personnumberlink'
        unique_together = (('person', 'number'),)
