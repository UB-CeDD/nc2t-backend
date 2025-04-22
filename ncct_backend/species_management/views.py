from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

from .models import Species
from .serializers import SpeciesSerializer


# List and Create View
class SpeciesListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Species.objects.all()
    serializer_class = SpeciesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'category', 'habitat']


# Retrieve, Update, and Delete View
class SpeciesRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Species.objects.all()
    serializer_class = SpeciesSerializer