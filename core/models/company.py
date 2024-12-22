from django.db import models
from .base import SearchableModel

class Company(SearchableModel):
    company = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    default_person = models.ForeignKey('Person', null=True, on_delete=models.SET_NULL, db_column='defaultPerson')
    default_phone = models.ForeignKey('Number', null=True, on_delete=models.SET_NULL, related_name='companies_phone', db_column='defaultNumber_phone')
    default_fax = models.ForeignKey('Number', null=True, on_delete=models.SET_NULL, related_name='companies_fax', db_column='defaultNumber_fax')
    company_types = models.ManyToManyField('CompanyType', through='CompanyCompanyTypeLink')
    company_properties = models.ManyToManyField('CompanyProperty', through='CompanyCompanyPropertyLink')
    locations = models.ManyToManyField('Location', through='CompanyLocationLink')
    emails = models.ManyToManyField('Email', through='CompanyEmailLink')
    
    class Meta:
        verbose_name_plural = 'companies'
    
    def __str__(self):
        return self.company

class CompanyType(models.Model):
    company_type = models.CharField(max_length=255, db_column='companyType')
    
    def __str__(self):
        return self.company_type

class CompanyProperty(models.Model):
    company_property = models.CharField(max_length=255, db_column='companyProperty')
    
    class Meta:
        verbose_name_plural = 'company properties'
    
    def __str__(self):
        return self.company_property