from rest_framework import serializers

from houmers.models import Location


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = ['latitude', 'longitude', 'altitude', 'date']

    def validate(self, data):
        """
        Check coordinates
        """
        if not -90.0 <= data['latitude'] <= 90.0 or not -180.0 <= data['longitude'] <= 180.0 \
                or not -500 <= data['altitude'] <= 10000:
            raise serializers.ValidationError("Invalid coordinates")
        return data


class TimeIntervalSerializer(serializers.Serializer):
    date_from = serializers.DateTimeField()
    date_to = serializers.DateTimeField()


class ReportsMoveParams(serializers.Serializer):
    user = serializers.CharField(max_length=200)
    date = serializers.DateField()
    speed = serializers.FloatField()
