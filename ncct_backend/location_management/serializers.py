from rest_framework import serializers
from .models import Location, Site

class LocationSerializer(serializers.ModelSerializer):
    voucher_specimen_number = serializers.CharField(max_length=255, required=False, allow_blank=True, allow_null=True)
    
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