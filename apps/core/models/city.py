from django.db import models

class City(models.Model):
    cityid = models.AutoField(db_column='cityID', primary_key=True)
    city = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'city'
