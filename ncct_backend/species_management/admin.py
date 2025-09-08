from django.contrib import admin
from .models import Species, Habitat, SpeciesUser, SpeciesChange
from ncct_backend.location_management.models import Site

@admin.register(Species)
class SpeciesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'family', 'publication_status', 'is_public')
    search_fields = ('name', 'family', 'references__title')
    list_filter = ('publication_status', 'is_public', 'family')
    filter_horizontal = ('compounds', 'references', 'storage_locations', 'habitats', 'users')

@admin.register(Habitat)
class HabitatAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(SpeciesUser)
class SpeciesUserAdmin(admin.ModelAdmin):
    list_display = ('species', 'user', 'role')
    search_fields = ('species__name', 'user__username')
    list_filter = ('role',)

@admin.register(SpeciesChange)
class SpeciesChangeAdmin(admin.ModelAdmin):
    list_display = ('species', 'user', 'status', 'created_at')
    search_fields = ('species__name', 'user__username')
    list_filter = ('status',)
    readonly_fields = ('created_at',)

@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    search_fields = ('name', 'location__name')
