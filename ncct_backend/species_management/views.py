from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

from .models import Species
from .serializers import SpeciesListSerializer, SpeciesDetailSerializer


# List and Create View
class SpeciesListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Species.objects.all()
    serializer_class = SpeciesListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['compound_code']


# Retrieve, Update, and Delete View
class SpeciesRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Species.objects.all()
    serializer_class = SpeciesDetailSerializer
