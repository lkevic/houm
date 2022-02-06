from rest_framework import serializers


def decimal_degrees(value):
    if not -180.0 <= value <= 180.0:
        raise serializers.ValidationError('This field must be decimal degrees.')
