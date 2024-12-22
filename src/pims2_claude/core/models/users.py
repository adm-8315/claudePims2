from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone

class Person(models.Model):
    first_name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=35)
    address = models.ForeignKey('core.Address', on_delete=models.SET_NULL, null=True)
    emails = models.ManyToManyField('core.Email', through='PersonEmailLink')
    numbers = models.ManyToManyField('core.Number', through='PersonNumberLink')

    class Meta:
        db_table = 'person'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Email(models.Model):
    user = models.CharField(max_length=58)
    domain = models.CharField(max_length=58)
    tld = models.CharField(max_length=6)

    class Meta:
        db_table = 'email'

    def __str__(self):
        return f'{self.user}@{self.domain}.{self.tld}'

    @property
    def full_email(self):
        return f'{self.user}@{self.domain}.{self.tld}'

class NumberType(models.Model):
    number_type = models.CharField(max_length=255)

    class Meta:
        db_table = 'numbertype'

class Number(models.Model):
    number_type = models.ForeignKey(NumberType, on_delete=models.PROTECT)
    number = models.CharField(max_length=10)
    ext = models.CharField(max_length=5, null=True)

    class Meta:
        db_table = 'number'

    def __str__(self):
        return f'{self.number} ({self.number_type})'

class PersonEmailLink(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    email = models.ForeignKey(Email, on_delete=models.CASCADE)
    is_primary = models.BooleanField(db_column='primary', default=False)

    class Meta:
        db_table = 'personemaillink'

class PersonNumberLink(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    number = models.ForeignKey(Number, on_delete=models.CASCADE)

    class Meta:
        db_table = 'personnumberlink'

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)

class User(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE)
    username = models.CharField(max_length=255, unique=True)
    password_hash = models.CharField(max_length=40)
    active = models.BooleanField(default=True)
    default_location = models.ForeignKey('core.Location', on_delete=models.PROTECT, related_name='default_for_users')
    default_owner = models.ForeignKey('core.Company', on_delete=models.PROTECT, related_name='default_owner_for_users')
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.username

class PermissionGroup(models.Model):
    permission_group = models.CharField(max_length=255)
    location_based = models.BooleanField(default=True)

    class Meta:
        db_table = 'permissiongroup'

class PermissionBlock(models.Model):
    permission_group = models.ForeignKey(PermissionGroup, on_delete=models.CASCADE)
    permission_block = models.CharField(max_length=255)
    permission_block_description = models.CharField(max_length=255, null=True)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'permissionblock'

class PermissionLink(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    permission_block = models.ForeignKey(PermissionBlock, on_delete=models.CASCADE)
    all_location = models.BooleanField(default=False)
    location = models.ForeignKey('core.Location', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'permissionlink'
