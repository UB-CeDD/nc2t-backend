from rest_framework import serializers
from .models import Location, Site

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class SiteSerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only=True)
    location_id = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all(), source='location', write_only=True
    )

    class Meta:
        model = Site
        fields = ['id', 'name', 'description', 'location', 'location_id']