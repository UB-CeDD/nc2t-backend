from rest_framework import serializers
from django.db import transaction
from .models import Species, SpeciesCompound, SpeciesSite, SpeciesHerbarium, Site, Herbarium
from ncct_backend.reference_management.serializers import ReferenceSerializer
from ncct_backend.compound_management.serializers import CompoundSerializer
from ncct_backend.location_management.serializers import LocationSerializer
from ncct_backend.reference_management.models import Reference
from ncct_backend.compound_management.models import Compound
from ncct_backend.location_management.models import Location


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


class SpeciesSerializer(serializers.ModelSerializer):
    compound_codes = serializers.SerializerMethodField()

    class Meta:
        model = Species
        fields = ['unique_id', 'name', 'recent_name', 'kingdom', 'family', 'compound_codes', 'references', 'collection_data']

    def get_compound_codes(self, obj):
        # Use SpeciesCompound join table to get all compound ids for this species
        return list(SpeciesCompound.objects.filter(species=obj).values_list('compound_id', flat=True))


class SpeciesDetailSerializer(SpeciesSerializer):
    references = ReferenceSerializer(many=True, read_only=True, source='references')
    compounds = SpeciesCompoundSerializer(many=True, read_only=True, source='speciescompound_set')
    sites = SpeciesSiteSerializer(many=True, read_only=True, source='speciessite_set')
    herbariums = SpeciesHerbariumSerializer(many=True, read_only=True, source='speciesherbarium_set')

    class Meta(SpeciesSerializer.Meta):
        model = Species
        fields = ('unique_id', 'compound_codes', 'references', 'collection_data', 'compounds', 'sites', 'herbariums', 'name', 'recent_name', 'kingdom', 'family')


class SpeciesListSerializer(SpeciesSerializer):
    references_data = serializers.ListField(
        child=serializers.DictField(), write_only=True, required=False
    )
    compound_data = serializers.ListField(
        child=serializers.DictField(), write_only=True, required=False
    )
    sites_data = serializers.ListField(
        child=serializers.DictField(), write_only=True, required=False
    )
    herbariums_data = serializers.ListField(
        child=serializers.DictField(), write_only=True, required=False
    )

    class Meta(SpeciesSerializer.Meta):
        model = Species
        fields = ('unique_id', 'compound_codes', 'collection_data', 'references_data', 'compound_data', 'sites_data', 'herbariums_data', 'name', 'recent_name', 'kingdom', 'family')

    @transaction.atomic
    def create(self, validated_data):
        references_data = validated_data.pop('references_data', [])
        compound_data = validated_data.pop('compound_data', [])
        sites_data = validated_data.pop('sites_data', [])
        herbariums_data = validated_data.pop('herbariums_data', [])

        # Create Species instance
        species = Species.objects.create(**validated_data)

        # Handle References
        for ref_data in references_data:
            reference, created = Reference.objects.get_or_create(title=ref_data.get('title'), defaults=ref_data)
            species.references.add(reference)

        # Handle Compounds
        for comp_data in compound_data:
            compound, created = Compound.objects.get_or_create(smiles=comp_data.get('smiles'), defaults=comp_data)
            SpeciesCompound.objects.create(species=species, compound=compound)

        # Handle Sites
        for site_data in sites_data:
            location_data = site_data.pop('location', {})
            location, created = Location.objects.get_or_create(name=location_data.get('name'), defaults=location_data)
            site, created = Site.objects.get_or_create(location=location, defaults=site_data)
            SpeciesSite.objects.create(species=species, site=site)

        # Handle Herbariums
        for herb_data in herbariums_data:
            location_data = herb_data.pop('location', {})
            location, created = Location.objects.get_or_create(name=location_data.get('name'), defaults=location_data)
            herbarium, created = Herbarium.objects.get_or_create(location=location, defaults=herb_data)
            SpeciesHerbarium.objects.create(species=species, herbarium=herbarium)

        return species
