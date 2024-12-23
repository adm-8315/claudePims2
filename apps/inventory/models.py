from django.db import models

class Item(models.Model):
    itemid = models.AutoField(db_column='itemID', primary_key=True)
    item = models.CharField(max_length=255, blank=True, null=True)
    itemtype = models.ForeignKey('Itemtype', models.DO_NOTHING, db_column='itemType')
    lastprice = models.CharField(db_column='lastPrice', max_length=255, blank=True, null=True)
    lastsupplier = models.CharField(db_column='lastSupplier', max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'item'

class Itemtype(models.Model):
    itemtypeid = models.AutoField(db_column='itemTypeID', primary_key=True)
    itemtype = models.CharField(db_column='itemType', max_length=255)

    class Meta:
        managed = False
        db_table = 'itemtype'

class Iteminventory(models.Model):
    iteminventoryid = models.AutoField(db_column='itemInventoryID', primary_key=True)
    item = models.ForeignKey(Item, models.DO_NOTHING, db_column='item')
    location = models.ForeignKey('core.Location', models.DO_NOTHING, db_column='location', blank=True, null=True)
    stock = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'iteminventory'
        unique_together = (('item', 'location'),)
