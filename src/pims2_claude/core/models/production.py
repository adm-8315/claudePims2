from django.db import models
from django.utils import timezone

class Form(models.Model):
    form_tag = models.CharField(max_length=4, blank=True, default='')
    form_location = models.CharField(max_length=255, blank=True, null=True)
    form_quantity = models.IntegerField(default=1)
    form_pieces = models.IntegerField(default=1)
    notes = models.CharField(max_length=255, null=True)
    products = models.ManyToManyField('Product', through='FormProductLink')

    class Meta:
        db_table = 'form'

    def __str__(self):
        return f'{self.form_tag} - {self.form_location}'

class FormProductLink(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)

    class Meta:
        db_table = 'formproductlink'

class Furnace(models.Model):
    furnace = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'furnace'

class FurnacePattern(models.Model):
    furnace = models.ForeignKey(Furnace, on_delete=models.CASCADE)
    furnace_pattern = models.CharField(max_length=255)
    pattern_description = models.CharField(max_length=255, null=True)
    pattern_temperature = models.IntegerField(null=True)
    pattern_time = models.IntegerField(null=True)

    class Meta:
        db_table = 'furnacepattern'

class ProductionOrder(models.Model):
    product = models.ForeignKey('Product', on_delete=models.PROTECT)
    quantity_ordered = models.IntegerField(null=True)
    quantity_filled = models.IntegerField(default=0)
    fill_date = models.DateField(null=True)
    notes = models.CharField(max_length=255, null=True)
    form = models.ForeignKey(Form, on_delete=models.SET_NULL, null=True)
    taps = models.IntegerField(null=True)
    lower_spec = models.FloatField(null=True)
    upper_spec = models.FloatField(null=True)
    furnace_pattern = models.ForeignKey(FurnacePattern, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey('User', on_delete=models.PROTECT)
    last_edit = models.DateTimeField(auto_now=True)
    active = models.IntegerField(default=1)
    materials = models.ManyToManyField('Material', through='ProductionOrderMaterialLink')

    class Meta:
        db_table = 'productionorder'

    def __str__(self):
        return f'PO-{self.id}: {self.product}'

class VibrationType(models.Model):
    vibration_type = models.CharField(max_length=7, null=True)

    class Meta:
        db_table = 'vibrationtype'

class ProductionOrderMaterialLink(models.Model):
    production_order = models.ForeignKey(ProductionOrder, on_delete=models.CASCADE)
    material = models.ForeignKey('Material', on_delete=models.CASCADE)
    quantity = models.FloatField(null=True)
    water = models.FloatField(null=True)
    mix_time = models.IntegerField(null=True)
    vibration_type = models.ForeignKey(VibrationType, on_delete=models.PROTECT, default=0)
    vibration_time = models.IntegerField(null=True)

    class Meta:
        db_table = 'productionordermateriallink'
        unique_together = ('material', 'production_order')

class ProductionOrderSchedule(models.Model):
    production_order = models.ForeignKey(ProductionOrder, on_delete=models.CASCADE)
    pour_date = models.DateField()
    strip_date = models.DateField()
    fire_date = models.DateField()
    quantity = models.IntegerField(default=0)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'productionorderschedule'
        unique_together = ('pour_date', 'production_order')

class ProductionOrderOption(models.Model):
    production_order_option_type = models.ForeignKey('ProductionOrderOptionType', on_delete=models.PROTECT)
    production_order_option = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'productionorderoption'

class ProductionOrderOptionType(models.Model):
    production_order_option_type = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'productionorderoptiontype'

class ProductionOrderTemplate(models.Model):
    product = models.ForeignKey('Product', on_delete=models.PROTECT)
    notes = models.CharField(max_length=255, null=True)
    form = models.ForeignKey(Form, on_delete=models.SET_NULL, null=True)
    taps = models.IntegerField(null=True)
    lower_spec = models.FloatField(null=True)
    upper_spec = models.FloatField(null=True)
    furnace_pattern = models.ForeignKey(FurnacePattern, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey('User', on_delete=models.PROTECT)
    last_edit = models.DateTimeField(auto_now=True)
    active = models.IntegerField(default=1)

    class Meta:
        db_table = 'productionordertemplate'
