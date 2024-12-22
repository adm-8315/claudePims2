from django.db import models
from django.utils import timezone

class ProductionOrder(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity_ordered = models.IntegerField(null=True, db_column='quantityOrdered')
    quantity_filled = models.IntegerField(default=0, db_column='quantityFilled')
    fill_date = models.DateField(null=True, db_column='fillDate')
    notes = models.CharField(max_length=255, null=True)
    form = models.ForeignKey('Form', null=True, on_delete=models.SET_NULL)
    taps = models.IntegerField(null=True)
    lower_spec = models.FloatField(null=True, db_column='lowerSpec')
    upper_spec = models.FloatField(null=True, db_column='upperSpec')
    furnace_pattern = models.ForeignKey('FurnacePattern', null=True, on_delete=models.SET_NULL, db_column='furnacePattern')
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    last_edit = models.DateTimeField(auto_now=True, db_column='lastEdit')
    active = models.IntegerField(default=1)
    materials = models.ManyToManyField('Material', through='ProductionOrderMaterialLink')
    options = models.ManyToManyField('ProductionOrderOption', through='ProductionOrderProductionOrderOptionLink')

    def __str__(self):
        return f'Order {self.id} - {self.product}'

class ProductionOrderMaterialLink(models.Model):
    production_order = models.ForeignKey(ProductionOrder, on_delete=models.CASCADE, db_column='productionOrder')
    material = models.ForeignKey('Material', on_delete=models.CASCADE)
    quantity = models.FloatField(null=True)
    water = models.FloatField(null=True)
    mix_time = models.IntegerField(null=True, db_column='mixTime')
    vibration_type = models.ForeignKey('VibrationType', on_delete=models.CASCADE, default=0, db_column='vibrationType')
    vibration_time = models.IntegerField(null=True, db_column='vibrationTime')

class ProductionOrderOption(models.Model):
    option_type = models.ForeignKey('ProductionOrderOptionType', on_delete=models.CASCADE, db_column='productionOrderOptionType')
    option = models.CharField(max_length=255, null=True, db_column='productionOrderOption')

    def __str__(self):
        return self.option

class ProductionOrderOptionType(models.Model):
    option_type = models.CharField(max_length=255, null=True, db_column='productionOrderOptionType')

    def __str__(self):
        return self.option_type

class ProductionOrderSchedule(models.Model):
    production_order = models.ForeignKey(ProductionOrder, on_delete=models.CASCADE, db_column='productionOrder')
    pour_date = models.DateField(db_column='pourDate')
    strip_date = models.DateField(db_column='stripDate')
    fire_date = models.DateField(db_column='fireDate')
    quantity = models.IntegerField(default=0)
    active = models.BooleanField(default=True)

    class Meta:
        unique_together = ['production_order', 'pour_date']