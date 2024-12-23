from django.db import models

class Location(models.Model):
    locationid = models.AutoField(db_column='locationID', primary_key=True)
    location = models.CharField(max_length=255)
    address = models.ForeignKey('Address', models.DO_NOTHING, db_column='address', blank=True, null=True)
    active = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'location'
