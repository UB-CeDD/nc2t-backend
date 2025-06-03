from django.urls import path
from .views import SpeciesListCreateView, SpeciesRetrieveUpdateDestroyView

urlpatterns = [
    path('species/', SpeciesListCreateView.as_view(), name='species-list-create'),
    path('species/<int:pk>/', SpeciesRetrieveUpdateDestroyView.as_view(), name='species-detail'),
]