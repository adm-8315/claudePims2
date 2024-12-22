from django.db import models
from .base import SearchableModel

class Location(SearchableModel):
    location = models.CharField(max_length=255)
    stockable = models.BooleanField(default=False)
    address = models.ForeignKey('Address', null=True, on_delete=models.SET_NULL)
    region = models.ForeignKey('Region', null=True, on_delete=models.SET_NULL)
    active = models.BooleanField(default=True)
    requirements = models.ManyToManyField('Requirement', through='LocationRequirementLink')
    
    def __str__(self):
        return self.location

class Address(models.Model):
    line_one = models.CharField(max_length=255, db_column='lineOne')
    line_two = models.CharField(max_length=255, null=True, db_column='lineTwo')
    line_three = models.CharField(max_length=255, null=True, db_column='lineThree')
    city = models.ForeignKey('City', on_delete=models.CASCADE)
    zip = models.CharField(max_length=6)
    state = models.ForeignKey('State', on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural = 'addresses'
    
    def __str__(self):
        return f'{self.line_one}, {self.city}, {self.state.short} {self.zip}'

class City(models.Model):
    city = models.CharField(max_length=255)
    
    class Meta:
        verbose_name_plural = 'cities'
    
    def __str__(self):
        return self.city

class State(models.Model):
    state = models.CharField(max_length=255)
    short = models.CharField(max_length=2)
    
    def __str__(self):
        return self.short

class Region(models.Model):
    region = models.CharField(max_length=40)
    
    def __str__(self):
        return self.region