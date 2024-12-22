from django.db import models
from .base import SearchableModel

class Material(SearchableModel):
    material_type = models.ForeignKey('MaterialType', on_delete=models.CASCADE, db_column='materialType')
    cost = models.DecimalField(max_digits=11, decimal_places=2)
    measure = models.ForeignKey('Measure', on_delete=models.CASCADE)
    material = models.CharField(max_length=255)
    water_low = models.FloatField(null=True, db_column='waterLow')
    water_high = models.FloatField(null=True, db_column='waterHigh')
    mix_low = models.IntegerField(null=True, db_column='mixLow')
    mix_high = models.IntegerField(null=True, db_column='mixHigh')
    taps = models.IntegerField(null=True)
    lower_spec = models.FloatField(null=True, db_column='lowerSpec')
    upper_spec = models.FloatField(null=True, db_column='upperSpec')
    std_water = models.FloatField(null=True, db_column='stdWater')
    std_mix = models.IntegerField(null=True, db_column='stdMix')
    manufacturers = models.ManyToManyField('Company', through='MaterialManufacturerLink')
    
    def __str__(self):
        return self.material

class MaterialType(models.Model):
    material_type = models.CharField(max_length=25, db_column='materialType')
    
    def __str__(self):
        return self.material_type

class Measure(models.Model):
    measure_plural = models.CharField(max_length=255, db_column='measurePlural')
    measure_singular = models.CharField(max_length=255, db_column='measureSingular')
    
    def __str__(self):
        return self.measure_singular