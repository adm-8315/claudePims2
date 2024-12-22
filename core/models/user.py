from django.db import models
from django.contrib.auth.models import AbstractUser
from .base import TimestampedModel

class Person(models.Model):
    first_name = models.CharField(max_length=70, db_column='firstName')
    last_name = models.CharField(max_length=35, db_column='lastName')
    address = models.ForeignKey('Address', null=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class User(TimestampedModel):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    username = models.CharField(max_length=255, unique=True)
    password_hash = models.CharField(max_length=40, db_column='passwordHash')
    default_location = models.ForeignKey('Location', on_delete=models.SET_DEFAULT, default=1, db_column='defaultLocation')
    default_owner = models.ForeignKey('Company', on_delete=models.SET_DEFAULT, default=47, db_column='defaultOwner')
    active = models.BooleanField(default=True)
    last_update = models.DateTimeField(null=True, db_column='lastUpdate')
    locations = models.ManyToManyField('Location', through='UserLocationLink', related_name='users')

    def __str__(self):
        return self.username