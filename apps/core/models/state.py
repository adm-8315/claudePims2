from django.db import models

class State(models.Model):
    stateid = models.AutoField(db_column='stateID', primary_key=True)
    state = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=2)

    class Meta:
        managed = False
        db_table = 'state'
