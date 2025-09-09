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

    class Meta:
        model = Species
        fields = [
            'id', 'name', 'recent_name', 'kingdom', 'family', 'trad_uses', 'part_used',
            'collection_data', 'publication_status', 'is_public', 'publication_date',
            'compounds', 'references', 'harvest_sites', 'storage_locations', 'habitats'
        ]

    def to_representation(self, instance):
        """
        Switch to a detailed serializer for representation.
        """
        serializer = SpeciesDetailSerializer(instance, context=self.context)
        return serializer.data


class SpeciesDetailSerializer(serializers.ModelSerializer):
    compounds = CompoundSerializer(many=True, read_only=True)
    references = ReferenceSerializer(many=True, read_only=True)
    harvest_sites = LocationSerializer(many=True, read_only=True)
    storage_locations = LocationSerializer(many=True, read_only=True)
    habitats = HabitatSerializer(many=True, read_only=True)
    users = SpeciesUserSerializer(many=True, read_only=True)
    changes = SpeciesChangeSerializer(many=True, read_only=True)

    class Meta:
        model = Species
        fields = [
            'id', 'name', 'recent_name', 'kingdom', 'family', 'trad_uses', 'part_used',
            'collection_data', 'publication_status', 'is_public', 'publication_date',
            'compounds', 'references', 'harvest_sites', 'storage_locations', 'habitats',
            'users', 'changes'
        ]


class SpeciesListSerializer(SpeciesSerializer):
    """
    Serializer for listing and creating species.
    Uses the base SpeciesSerializer which is configured for write operations.
    """
    pass
