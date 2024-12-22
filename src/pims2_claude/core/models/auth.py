"""Authentication models for PIMS2 Claude integration."""
from datetime import datetime
from typing import List, Optional
from uuid import UUID
from django.db import models

class User(models.Model):
    """User model for authentication and authorization."""
    id = models.UUIDField(primary_key=True, default=UUID)
    username = models.CharField(max_length=150, unique=True)
    is_active = models.BooleanField(default=True)
    permissions = models.JSONField(default=list)
    last_login = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'

class AuthToken(models.Model):
    """Authentication token model."""
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    access_token = models.TextField()
    refresh_token = models.TextField()
    token_type = models.CharField(max_length=50, default="bearer")
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'auth_tokens'