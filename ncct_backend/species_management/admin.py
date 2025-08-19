from django.contrib import admin
from .models import Species, Site, Herbarium, SpeciesCompound, SpeciesSite, SpeciesHerbarium


@admin.register(Species)
class SpeciesAdmin(admin.ModelAdmin):
    list_display = ('unique_id', 'compound_code', 'ref', 'collection_data')
    search_fields = ('compound_code',)


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