from django.db import models

class State(models.Model):
    state = models.CharField(max_length=255)
    short = models.CharField(max_length=2)

    class Meta:
        db_table = 'state'

    def __str__(self):
        return self.short

class City(models.Model):
    city = models.CharField(max_length=255)

    class Meta:
        db_table = 'city'
        verbose_name_plural = 'cities'

    def __str__(self):
        return self.city

class Address(models.Model):
    line_one = models.CharField(max_length=255)
    line_two = models.CharField(max_length=255, null=True, blank=True)
    line_three = models.CharField(max_length=255, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    zip = models.CharField(max_length=6)
    state = models.ForeignKey(State, on_delete=models.PROTECT)

    class Meta:
        db_table = 'address'
        verbose_name_plural = 'addresses'

    def __str__(self):
        return f'{self.line_one}, {self.city}, {self.state}'

class Region(models.Model):
    region = models.CharField(max_length=40, null=True)

    class Meta:
        db_table = 'region'

    def __str__(self):
        return self.region

class Location(models.Model):
    location = models.CharField(max_length=255)
    stockable = models.BooleanField(default=False)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)
    active = models.BooleanField(default=True)
    search_count = models.IntegerField(default=0)

    class Meta:
        db_table = 'location'

    def __str__(self):
        return self.location

class CompanyType(models.Model):
    company_type = models.CharField(max_length=255)

    class Meta:
        db_table = 'companytype'

    def __str__(self):
        return self.company_type

class CompanyProperty(models.Model):
    company_property = models.CharField(max_length=255)

    class Meta:
        db_table = 'companyproperty'
        verbose_name_plural = 'Company Properties'

class Company(models.Model):
    company = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    default_person = models.ForeignKey('core.Person', on_delete=models.SET_NULL, null=True, related_name='default_for_companies')
    default_number_phone = models.ForeignKey('core.Number', on_delete=models.SET_NULL, null=True, related_name='default_phone_for_companies')
    default_number_fax = models.ForeignKey('core.Number', on_delete=models.SET_NULL, null=True, related_name='default_fax_for_companies')
    search_count = models.IntegerField(default=0)
    company_types = models.ManyToManyField(CompanyType, through='CompanyCompanyTypeLink')
    company_properties = models.ManyToManyField(CompanyProperty, through='CompanyCompanyPropertyLink')

    class Meta:
        db_table = 'company'
        verbose_name_plural = 'companies'

    def __str__(self):
        return self.company

class CompanyCompanyTypeLink(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    company_type = models.ForeignKey(CompanyType, on_delete=models.CASCADE)

    class Meta:
        db_table = 'companycompanytypelink'
        unique_together = ('company', 'company_type')

class CompanyCompanyPropertyLink(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    company_property = models.ForeignKey(CompanyProperty, on_delete=models.CASCADE)

    class Meta:
        db_table = 'companycompanypropertylink'
        unique_together = ('company', 'company_property')

class CompanyLocationLink(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    numbers = models.ManyToManyField('core.Number', through='CompanyLocationLinkNumberLink')
    persons = models.ManyToManyField('core.Person', through='CompanyLocationLinkPersonLink')

    class Meta:
        db_table = 'companylocationlink'

    def __str__(self):
        return f'{self.company} at {self.location}' if self.company else f'{self.location}'
