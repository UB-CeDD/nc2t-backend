from rest_framework import serializers
from .models import Species, SpeciesCompound, SpeciesSite, SpeciesHerbarium, Site, Herbarium
from ncct_backend.reference_management.serializers import ReferenceSerializer
from ncct_backend.compound_management.serializers import CompoundSerializer
from ncct_backend.location_management.serializers import LocationSerializer


class SiteSerializer(serializers.ModelSerializer):
    location = LocationSerializer()

    class Meta:
        model = Site
        fields = '__all__'


class HerbariumSerializer(serializers.ModelSerializer):
    location = LocationSerializer()

    class Meta:
        model = Herbarium
        fields = '__all__'


class SpeciesCompoundSerializer(serializers.ModelSerializer):
    compound = CompoundSerializer()

    class Meta:
        model = SpeciesCompound
        fields = ('compound',)


class SpeciesSiteSerializer(serializers.ModelSerializer):
    site = SiteSerializer()

    class Meta:
        model = SpeciesSite
        fields = ('site',)


class SpeciesHerbariumSerializer(serializers.ModelSerializer):
    herbarium = HerbariumSerializer()

    class Meta:
        model = SpeciesHerbarium
        fields = ('herbarium',)


class SpeciesDetailSerializer(serializers.ModelSerializer):
    ref = ReferenceSerializer()
    compounds = SpeciesCompoundSerializer(many=True, read_only=True, source='speciescompound_set')
    sites = SpeciesSiteSerializer(many=True, read_only=True, source='speciessite_set')
    herbariums = SpeciesHerbariumSerializer(many=True, read_only=True, source='speciesherbarium_set')

    class Meta:
        model = Species
        fields = ('unique_id', 'compound_code', 'ref', 'collection_data', 'compounds', 'sites', 'herbariums')


class SpeciesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Species
        fields = ('unique_id', 'compound_code', 'collection_data')
