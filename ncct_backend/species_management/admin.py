from django.contrib import admin
from .models import Species, Site, Herbarium, SpeciesCompound, SpeciesSite, SpeciesHerbarium
from ncct_backend.reference_management.models import Reference # Import Reference model


@admin.register(Species)
class SpeciesAdmin(admin.ModelAdmin):
    list_display = ('unique_id', 'compound_codes_display', 'display_references', 'collection_data')
    search_fields = ('references__title',)

    def compound_codes_display(self, obj):
        return ', '.join(str(sc.compound_id) for sc in obj.speciescompound_set.all())
    compound_codes_display.short_description = 'Compound IDs'

    def display_references(self, obj):
        return ", ".join([ref.title for ref in obj.references.all()])
    display_references.short_description = 'References'


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ('unique_id', 'location')


@admin.register(Herbarium)
class HerbariumAdmin(admin.ModelAdmin):
    list_display = ('unique_id', 'location')


@admin.register(SpeciesCompound)
class SpeciesCompoundAdmin(admin.ModelAdmin):
    list_display = ('species', 'compound')


@admin.register(SpeciesSite)
class SpeciesSiteAdmin(admin.ModelAdmin):
    list_display = ('species', 'site')


@admin.register(SpeciesHerbarium)
class SpeciesHerbariumAdmin(admin.ModelAdmin):
    list_display = ('species', 'herbarium')