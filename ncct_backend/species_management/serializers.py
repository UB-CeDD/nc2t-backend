from rest_framework import serializers
from .models import Species, SpeciesUser, SpeciesChange, Habitat, Herbarium
from ncct_backend.reference_management.serializers import ReferenceSerializer
from ncct_backend.compound_management.serializers import CompoundSerializer
from ncct_backend.location_management.serializers import LocationSerializer, SiteSerializer
from ncct_backend.reference_management.models import Reference
from ncct_backend.compound_management.models import Compound
from ncct_backend.location_management.models import Location, Site


class HerbariumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Herbarium
        fields = '__all__'


class HabitatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habitat
        fields = '__all__'


class SpeciesUserSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = SpeciesUser
        fields = ['id', 'species', 'user', 'username', 'role']
        read_only_fields = ['species']


class SpeciesChangeSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    approved_by_username = serializers.ReadOnlyField(source='approved_by.username')

    class Meta:
        model = SpeciesChange
        fields = ['id', 'species', 'user', 'username', 'changes', 'status', 'created_at', 'approved_by', 'approved_by_username']
        read_only_fields = ['species', 'user', 'status', 'created_at', 'approved_by']


class SpeciesSerializer(serializers.ModelSerializer):
    # Use PrimaryKeyRelatedField for write operations, but allow for nested reading
    compounds = serializers.PrimaryKeyRelatedField(
        queryset=Compound.objects.all(), many=True, allow_empty=False
    )
    references = serializers.PrimaryKeyRelatedField(
        queryset=Reference.objects.all(), many=True, allow_empty=False
    )
    harvest_sites = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all(), many=True, allow_empty=False
    )
    storage_locations = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all(), many=True, required=True
    )

    class Meta:
        model = Species
        fields = [
            'id', 'name', 'recent_name', 'kingdom', 'family', 'trad_uses', 'part_used',
            'collection_data', 'publication_status', 'is_public', 'publication_date',
            'compounds', 'references', 'harvest_sites', 'storage_locations', 'habitats'
        ]




class SpeciesDetailSerializer(serializers.ModelSerializer):
    # Read-only nested views for GET requests
    compounds_detail = CompoundSerializer(many=True, read_only=True, source='compounds')
    references_detail = ReferenceSerializer(many=True, read_only=True, source='references')
    harvest_sites_detail = LocationSerializer(many=True, read_only=True, source='harvest_sites')
    storage_locations_detail = LocationSerializer(many=True, read_only=True, source='storage_locations')
    habitats_detail = HabitatSerializer(many=True, read_only=True, source='habitats')
    
    # Writable fields for updates
    compounds = serializers.PrimaryKeyRelatedField(
        queryset=Compound.objects.all(), many=True, required=False
    )
    references = serializers.PrimaryKeyRelatedField(
        queryset=Reference.objects.all(), many=True, required=False
    )
    harvest_sites = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all(), many=True, required=False
    )
    storage_locations = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all(), many=True, required=False
    )
    habitats = serializers.PrimaryKeyRelatedField(
        queryset=Habitat.objects.all(), many=True, required=False
    )
    
    users = SpeciesUserSerializer(many=True, read_only=True, source='speciesuser_set')
    changes = SpeciesChangeSerializer(many=True, read_only=True)

    class Meta:
        model = Species
        fields = [
            'id', 'name', 'recent_name', 'kingdom', 'family', 'trad_uses', 'part_used',
            'collection_data', 'publication_status', 'is_public', 'publication_date',
            'compounds', 'compounds_detail', 'references', 'references_detail',
            'harvest_sites', 'harvest_sites_detail', 'storage_locations', 'storage_locations_detail',
            'habitats', 'habitats_detail', 'users', 'changes'
        ]


class SpeciesListSerializer(SpeciesSerializer):
    """
    Serializer for listing and creating species.
    Uses the base SpeciesSerializer which is configured for write operations.
    """
    def create(self, validated_data):
        # Get the user from the context
        user = self.context['request'].user

        # Create the species instance
        species = super().create(validated_data)

        # Assign the user as an author
        SpeciesUser.objects.create(species=species, user=user, role='AUTHOR')

        return species
