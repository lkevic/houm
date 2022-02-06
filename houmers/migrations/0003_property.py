# Generated by Django 4.0.2 on 2022-02-06 19:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('houmers', '0002_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField(help_text='Location latitude. Must be expressed in decimal degrees.')),
                ('longitude', models.FloatField(help_text='Location longitude. Must be expressed in decimal degrees.')),
                ('tolerance_radius', models.FloatField(default=25.0, help_text='Tolerance radios. All coordinates within the tolerance radius of the property will be considered visits to the property.Must be expressed in meters. By default it will be set to 25 meters')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Property creation date')),
                ('modified_at', models.DateTimeField(auto_now=True, help_text='Property last modified date')),
                ('created_by', models.ForeignKey(help_text='User who created the property', on_delete=django.db.models.deletion.PROTECT, related_name='created_properties_set', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(help_text='Last user who modified the property', on_delete=django.db.models.deletion.PROTECT, related_name='modified_properties_set', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
