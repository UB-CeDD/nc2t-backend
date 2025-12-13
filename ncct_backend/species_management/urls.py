from django.urls import path
from .views import (
    SpeciesListCreateView,
    SpeciesRetrieveUpdateDestroyView,
    SpeciesUserListCreateView,
    SpeciesUserRetrieveUpdateDestroyView,
    SpeciesChangeListCreateView,
    SpeciesChangeRetrieveUpdateDestroyView,
    HabitatListCreateView,
    HabitatRetrieveUpdateDestroyView,
    HerbariumListCreateView,
    HerbariumRetrieveUpdateDestroyView,
)

urlpatterns = [
    path('species/', SpeciesListCreateView.as_view(), name='species-list-create'),
    path('species/<slug:pk>/', SpeciesRetrieveUpdateDestroyView.as_view(), name='species-detail'),
    path('species/<slug:species_pk>/users/', SpeciesUserListCreateView.as_view(), name='species-user-list-create'),
    path('species/<slug:species_pk>/users/<int:pk>/', SpeciesUserRetrieveUpdateDestroyView.as_view(), name='species-user-detail'),
    path('species/<slug:species_pk>/changes/', SpeciesChangeListCreateView.as_view(), name='species-change-list-create'),
    path('species/<slug:species_pk>/changes/<int:pk>/', SpeciesChangeRetrieveUpdateDestroyView.as_view(), name='species-change-detail'),
    path('habitats/', HabitatListCreateView.as_view(), name='habitat-list-create'),
    path('habitats/<slug:pk>/', HabitatRetrieveUpdateDestroyView.as_view(), name='habitat-detail'),
    path('herbariums/', HerbariumListCreateView.as_view(), name='herbarium-list-create'),
    path('herbariums/<slug:pk>/', HerbariumRetrieveUpdateDestroyView.as_view(), name='herbarium-detail'),
]
