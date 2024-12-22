from django.db import models
from django.utils import timezone

class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class SearchableModel(models.Model):
    search_count = models.IntegerField(default=0, db_column='searchCount')
    
    class Meta:
        abstract = True