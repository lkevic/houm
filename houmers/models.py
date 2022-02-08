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


class Property(models.Model):
    latitude = models.FloatField(help_text='Location latitude. Must be expressed in decimal degrees.')
    longitude = models.FloatField(help_text='Location longitude. Must be expressed in decimal degrees.')
    tolerance_radius = models.FloatField(
        help_text='Tolerance radios. All coordinates within the tolerance radius of the property will be considered '
                  'visits to the property.Must be expressed in meters. By default it will be set to 25 meters',
        default=25.0)
    created_at = models.DateTimeField(auto_now_add=True, help_text='Property creation date')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                                   related_name='created_properties_set', help_text='User who created the property')
    modified_at = models.DateTimeField(auto_now=True, help_text='Property last modified date')
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                                    related_name='modified_properties_set',
                                    help_text='Last user who modified the property')

    max_latitude = models.FloatField()
    min_latitude = models.FloatField()
    max_longitude = models.FloatField()
    min_longitude = models.FloatField()

    def save(self, *args, **kwargs):

        meters_in_one_degrees = 111.4 * 1000

        aux = self.latitude + self.tolerance_radius / meters_in_one_degrees
        self.max_latitude = aux if aux < 90.0 else 90.0
        aux = self.latitude - self.tolerance_radius / meters_in_one_degrees
        self.min_latitude = aux if aux > -90.0 else -90.0

        aux = self.longitude + self.tolerance_radius / meters_in_one_degrees
        self.max_longitude = aux if aux < 180.0 else 180.0
        aux = self.longitude - self.tolerance_radius / meters_in_one_degrees
        self.min_longitude = aux if aux > -180.0 else -180.0

        super(Property, self).save(*args, **kwargs)
