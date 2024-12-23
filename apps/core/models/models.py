from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType

class Address(models.Model):
    addressid = models.AutoField(db_column='addressID', primary_key=True)
    lineone = models.CharField(db_column='lineOne', max_length=255)
    linetwo = models.CharField(db_column='lineTwo', max_length=255, blank=True, null=True)
    linethree = models.CharField(db_column='lineThree', max_length=255, blank=True, null=True)
    city = models.ForeignKey('City', models.DO_NOTHING, db_column='city')
    zip = models.CharField(max_length=6)
    state = models.ForeignKey('State', models.DO_NOTHING, db_column='state')

    class Meta:
        db_table = 'address'
        
# Continue with your other models...

class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey(ContentType, models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING)

    class Meta:
        db_table = 'django_admin_log'