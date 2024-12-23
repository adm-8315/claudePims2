from django.db import models

class Address(models.Model):
    addressid = models.AutoField(db_column='addressID', primary_key=True)
    lineone = models.CharField(db_column='lineOne', max_length=255)
    linetwo = models.CharField(db_column='lineTwo', max_length=255, blank=True, null=True)
    linethree = models.CharField(db_column='lineThree', max_length=255, blank=True, null=True)
    city = models.ForeignKey('City', models.DO_NOTHING, db_column='city')
    zip = models.CharField(max_length=6)
    state = models.ForeignKey('State', models.DO_NOTHING, db_column='state')

    class Meta:
        managed = False
        db_table = 'address'
