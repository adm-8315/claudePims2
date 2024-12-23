from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """Custom user model for PIMS2."""
    
    class Meta:
        db_table = 'auth_user'
        
    def __str__(self):
        return self.username