from rest_framework import serializers

from houmers.models import Location, Property


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = ['latitude', 'longitude', 'altitude', 'date']

    def validate(self, data):
        """
        Check coordinates
        """
        if not -90.0 <= data['latitude'] <= 90.0 or not -180.0 <= data['longitude'] <= 180.0 \
                or not (data['altitude'] is not None and -500 <= data['altitude'] <= 10000):
            raise serializers.ValidationError("Invalid coordinates")
        return data


class PropertySerializer(serializers.ModelSerializer):

    class Meta:
        model = Property
        fields = ['id', 'latitude', 'longitude', 'tolerance_radius']
        read_only_fields = ['id']
        extra_kwargs = {'id': {'help_text': 'Property ID'}}

    def validate(self, data):
        """
        Check coordinates
        """
        if not -90.0 <= data['latitude'] <= 90.0 or not -180.0 <= data['longitude'] <= 180.0:
            raise serializers.ValidationError("Invalid coordinates")
        return data


class TimeIntervalSerializer(serializers.Serializer):
    date_from = serializers.DateTimeField()
    date_to = serializers.DateTimeField()


class VisitSerializer(serializers.Serializer):
    duration = serializers.DurationField()
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()


class ReportsMoveParams(serializers.Serializer):
    user = serializers.CharField(max_length=150)
    date = serializers.DateField()
    speed = serializers.FloatField()


class ReportsVisitParams(serializers.Serializer):
    user = serializers.CharField(max_length=150)
    date = serializers.DateField()
