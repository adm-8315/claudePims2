from django.db import models
from django.conf import settings

class Item(models.Model):
    itemid = models.AutoField(db_column='itemID', primary_key=True)
    item = models.CharField(max_length=255, blank=True, null=True)
    itemtype = models.ForeignKey('Itemtype', models.CASCADE, db_column='itemType')
    lastprice = models.CharField(db_column='lastPrice', max_length=255, blank=True, null=True)
    lastsupplier = models.CharField(db_column='lastSupplier', max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'item'

class Itemtype(models.Model):
    itemtypeid = models.AutoField(db_column='itemTypeID', primary_key=True)
    itemtype = models.CharField(db_column='itemType', max_length=255)

    class Meta:
        db_table = 'itemtype'

class Iteminventory(models.Model):
    iteminventoryid = models.AutoField(db_column='itemInventoryID', primary_key=True)
    item = models.ForeignKey(Item, models.CASCADE, db_column='item')
    location = models.ForeignKey('core.Location', models.SET_NULL, db_column='location', blank=True, null=True)
    stock = models.PositiveIntegerField()

    class Meta:
        db_table = 'iteminventory'
        unique_together = (('item', 'location'),)

class Measure(models.Model):
    measureid = models.AutoField(db_column='measureID', primary_key=True)
    measure = models.CharField(max_length=255)

    class Meta:
        db_table = 'measure'

class MaterialType(models.Model):
    materialtypeid = models.AutoField(db_column='materialTypeID', primary_key=True)
    materialtype = models.CharField(db_column='materialType', max_length=255)

    class Meta:
        db_table = 'materialtype'

class Material(models.Model):
    materialid = models.AutoField(db_column='materialID', primary_key=True)
    material = models.CharField(max_length=255)
    materialtype = models.ForeignKey(MaterialType, models.CASCADE, db_column='materialType')
    measure = models.ForeignKey(Measure, models.CASCADE, db_column='measure')

    class Meta:
        db_table = 'material'

class MaterialInventory(models.Model):
    materialinventoryid = models.AutoField(db_column='materialInventoryID', primary_key=True)
    material = models.ForeignKey(Material, models.CASCADE, db_column='material')
    companylocationlink = models.ForeignKey('core.CompanyLocationLink', models.CASCADE, db_column='companyLocationLink')
    stock = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'materialinventory'
        unique_together = (('material', 'companylocationlink'),)

class TransactionType(models.Model):
    transactiontypeid = models.AutoField(db_column='transactionTypeID', primary_key=True)
    transactiontype = models.CharField(db_column='transactionType', max_length=255)

    class Meta:
        db_table = 'transactiontype'

class MaterialTransaction(models.Model):
    materialtransactionid = models.AutoField(db_column='materialTransactionID', primary_key=True)
    materialinventory = models.ForeignKey(MaterialInventory, models.CASCADE, db_column='materialInventory')
    transactiontype = models.ForeignKey(TransactionType, models.CASCADE, db_column='transactionType')
    companylocationlink = models.ForeignKey('core.CompanyLocationLink', models.CASCADE, db_column='companyLocationLink')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, db_column='user')
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    transactiondate = models.DateTimeField(db_column='transactionDate', auto_now_add=True)

    class Meta:
        db_table = 'materialtransaction'

class ProductType(models.Model):
    producttypeid = models.AutoField(db_column='productTypeID', primary_key=True)
    producttype = models.CharField(db_column='productType', max_length=255)

    class Meta:
        db_table = 'producttype'

class Product(models.Model):
    productid = models.AutoField(db_column='productID', primary_key=True)
    product = models.CharField(max_length=255)
    producttype = models.ForeignKey(ProductType, models.CASCADE, db_column='productType')

    class Meta:
        db_table = 'product'

class ProductInventory(models.Model):
    productinventoryid = models.AutoField(db_column='productInventoryID', primary_key=True)
    product = models.ForeignKey(Product, models.CASCADE, db_column='product')
    companylocationlink = models.ForeignKey('core.CompanyLocationLink', models.CASCADE, db_column='companyLocationLink')
    stock = models.IntegerField()

    class Meta:
        db_table = 'productinventory'
        unique_together = (('product', 'companylocationlink'),)

class ProductTransaction(models.Model):
    producttransactionid = models.AutoField(db_column='productTransactionID', primary_key=True)
    productinventory = models.ForeignKey(ProductInventory, models.CASCADE, db_column='productInventory')
    transactiontype = models.ForeignKey(TransactionType, models.CASCADE, db_column='transactionType')
    companylocationlink = models.ForeignKey('core.CompanyLocationLink', models.CASCADE, db_column='companyLocationLink')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, db_column='user')
    quantity = models.IntegerField()
    transactiondate = models.DateTimeField(db_column='transactionDate', auto_now_add=True)

    class Meta:
        db_table = 'producttransaction'

class MaterialManufacturerLink(models.Model):
    material = models.ForeignKey(Material, models.CASCADE, db_column='material')
    company = models.ForeignKey('core.Company', models.CASCADE, db_column='company')

    class Meta:
        db_table = 'materialmanufacturerlink'
        unique_together = (('material', 'company'),)

class ProductConsumerLink(models.Model):
    product = models.ForeignKey(Product, models.CASCADE, db_column='product')
    companylocationlink = models.ForeignKey('core.CompanyLocationLink', models.CASCADE, db_column='companyLocationLink')

    class Meta:
        db_table = 'productconsumerlink'
        unique_together = (('product', 'companylocationlink'),)
