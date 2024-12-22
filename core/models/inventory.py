from django.db import models

class MaterialInventory(models.Model):
    material = models.ForeignKey('Material', on_delete=models.CASCADE)
    company_location_link = models.ForeignKey('CompanyLocationLink', null=True, on_delete=models.SET_NULL, db_column='companyLocationLink')
    stock = models.IntegerField()
    in_progress = models.IntegerField(default=0, db_column='inProgress')
    stock_level_warning = models.IntegerField(default=0, db_column='stockLevelWarning')

    class Meta:
        verbose_name_plural = 'material inventories'
        unique_together = ['material', 'company_location_link']

    def __str__(self):
        return f'{self.material} - {self.stock}'

class ProductInventory(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    company_location_link = models.ForeignKey('CompanyLocationLink', null=True, on_delete=models.SET_NULL, db_column='companyLocationLink')
    stock = models.IntegerField()
    in_progress = models.IntegerField(default=0, db_column='inProgress')
    stock_level_warning = models.IntegerField(default=0, db_column='stockLevelWarning')

    class Meta:
        verbose_name_plural = 'product inventories'
        unique_together = ['product', 'company_location_link']

    def __str__(self):
        return f'{self.product} - {self.stock}'

class MaterialTransaction(models.Model):
    material_inventory = models.ForeignKey(MaterialInventory, on_delete=models.CASCADE, db_column='materialInventory')
    transaction_type = models.ForeignKey('TransactionType', on_delete=models.CASCADE, db_column='transactionType')
    value = models.IntegerField()
    cost = models.FloatField(null=True)
    company_location_link = models.ForeignKey('CompanyLocationLink', null=True, on_delete=models.SET_NULL, db_column='companyLocationLink')
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    timestamp = models.DateField()
    notes = models.CharField(max_length=255, null=True)

class ProductTransaction(models.Model):
    product_inventory = models.ForeignKey(ProductInventory, on_delete=models.CASCADE, db_column='productInventory')
    transaction_type = models.ForeignKey('TransactionType', on_delete=models.CASCADE, db_column='transactionType')
    value = models.IntegerField()
    cost = models.FloatField(null=True)
    company_location_link = models.ForeignKey('CompanyLocationLink', null=True, on_delete=models.SET_NULL, db_column='companyLocationLink')
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    timestamp = models.DateField()
    notes = models.CharField(max_length=255, null=True)

class TransactionType(models.Model):
    transaction_type = models.CharField(max_length=255, db_column='transactionType')

    def __str__(self):
        return self.transaction_type