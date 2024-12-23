from django.db import models

class ProductType(models.Model):
    product_type = models.CharField(max_length=255)

    class Meta:
        db_table = 'producttype'

    def __str__(self):
        return self.product_type

class Product(models.Model):
    product_type = models.ForeignKey(ProductType, on_delete=models.PROTECT)
    cost = models.DecimalField(max_digits=11, decimal_places=2, null=True)
    measure = models.IntegerField(null=True)
    product = models.CharField(max_length=255, null=True)
    search_count = models.IntegerField(default=0)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'product'

    def __str__(self):
        return f'{self.product} ({self.product_type})'

class ProductInventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    company_location_link = models.IntegerField(null=True)
    stock = models.PositiveIntegerField()
    in_progress = models.PositiveIntegerField(default=0)
    stock_level_warning = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'productinventory'
        verbose_name_plural = 'Product Inventories'

class MaterialType(models.Model):
    material_type = models.CharField(max_length=25)

    class Meta:
        db_table = 'materialtype'

    def __str__(self):
        return self.material_type

class Material(models.Model):
    material_type = models.ForeignKey(MaterialType, on_delete=models.PROTECT)
    cost = models.DecimalField(max_digits=11, decimal_places=2)
    measure = models.IntegerField()
    material = models.CharField(max_length=255)
    water_low = models.FloatField(null=True)
    water_high = models.FloatField(null=True)
    mix_low = models.IntegerField(null=True)
    mix_high = models.IntegerField(null=True)
    taps = models.IntegerField(null=True)
    lower_spec = models.FloatField(null=True)
    upper_spec = models.FloatField(null=True)
    std_water = models.FloatField(null=True)
    std_mix = models.IntegerField(null=True)
    search_count = models.IntegerField(default=0)

    class Meta:
        db_table = 'material'

    def __str__(self):
        return f'{self.material} ({self.material_type})'

class MaterialInventory(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    company_location_link = models.IntegerField(null=True)
    stock = models.PositiveIntegerField()
    in_progress = models.PositiveIntegerField(default=0)
    stock_level_warning = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'materialinventory'
        verbose_name_plural = 'Material Inventories'