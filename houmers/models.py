from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class HoumerUser(AbstractUser):
    is_admin = models.BooleanField(default=False)


class Location(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='locations_set',
                             help_text='User')
    latitude = models.FloatField(help_text='Location latitude. Must be expressed in decimal degrees.')
    longitude = models.FloatField(help_text='Location longitude. Must be expressed in decimal degrees.')
    altitude = models.FloatField(help_text='Location longitude. Must be expressed in meters.')
    date = models.DateTimeField(help_text='Location date.')
    created_at = models.DateTimeField(auto_now_add=True)
