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
        if not -180.0 <= data['latitude'] <= 180.0 or not -180.0 <= data['longitude'] <= 180.0 \
                or not -500 <= data['altitude'] <= 10000:
            raise serializers.ValidationError("Invalid coordinates")
        return data
