from django.db import models
from django.contrib.auth.models import AbstractUser

from .mixins import PrimaryKeyMixin, LocationMixin

# Create your models here.

__all__ = ['User',]

USER_GENDER_CHOICES = (('MALE', 'MALE'), ('FEMALE', 'FEMALE'))


class User(AbstractUser, PrimaryKeyMixin, LocationMixin):
    first_name = None
    last_name = None

    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    full_name = models.CharField(max_length=255)
    bio = models.CharField(max_length=455)
    date_of_birth = models.DateField(null=True, blank=True)

    gender = models.CharField(choices=USER_GENDER_CHOICES, max_length=15, default='MALE')
    profile_photo = models.FileField(upload_to='profile/profile_pictures', blank=True, null=True)

    is_private = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'full_name')
