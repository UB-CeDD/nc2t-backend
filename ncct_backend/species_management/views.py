from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Species, SpeciesUser, SpeciesChange, Habitat, Herbarium
from .serializers import (
    SpeciesListSerializer, SpeciesDetailSerializer, SpeciesUserSerializer, 
    SpeciesChangeSerializer, HabitatSerializer, HerbariumSerializer
)

# List and Create View for Species
class SpeciesListCreateView(ListCreateAPIView):
    queryset = Species.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['family', 'publication_status', 'is_public', 'habitats__name']
    search_fields = ['name', 'recent_name', 'family']

    def get_permissions(self):
        if self.request.method in ['GET', 'HEAD', 'OPTIONS']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SpeciesListSerializer
        return SpeciesDetailSerializer

# Retrieve, Update, and Delete View for Species
class SpeciesRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Species.objects.all()
    serializer_class = SpeciesDetailSerializer

    def get_permissions(self):
        if self.request.method in ['GET', 'HEAD', 'OPTIONS']:
            return [AllowAny()]
        return [IsAuthenticated()]

# List and Create View for SpeciesUser
class SpeciesUserListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SpeciesUserSerializer

    def get_queryset(self):
        species_pk = self.kwargs['species_pk']
        return SpeciesUser.objects.filter(species_id=species_pk)

    def perform_create(self, serializer):
        species_pk = self.kwargs['species_pk']
        species = Species.objects.get(id=species_pk)
        serializer.save(species=species)

# Retrieve, Update, and Delete View for SpeciesUser
class SpeciesUserRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SpeciesUserSerializer

    def get_queryset(self):
        species_pk = self.kwargs['species_pk']
        return SpeciesUser.objects.filter(species_id=species_pk)

# List and Create View for SpeciesChange
class SpeciesChangeListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SpeciesChangeSerializer

    def get_queryset(self):
        species_pk = self.kwargs['species_pk']
        return SpeciesChange.objects.filter(species_id=species_pk)

    def perform_create(self, serializer):
        species_pk = self.kwargs['species_pk']
        species = Species.objects.get(id=species_pk)
        serializer.save(species=species, user=self.request.user)

# Retrieve, Update, and Delete View for SpeciesChange
class SpeciesChangeRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SpeciesChangeSerializer

    def get_queryset(self):
        species_pk = self.kwargs['species_pk']
        return SpeciesChange.objects.filter(species_id=species_pk)

# List and Create View for Habitat
class HabitatListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Habitat.objects.all()
    serializer_class = HabitatSerializer
    filter_backends = [DjangoFilterBackend]
    search_fields = ['name']

# Retrieve, Update, and Delete View for Habitat
class HabitatRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Habitat.objects.all()
    serializer_class = HabitatSerializer

# List and Create View for Herbarium
class HerbariumListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Herbarium.objects.all()
    serializer_class = HerbariumSerializer
    filter_backends = [DjangoFilterBackend]
    search_fields = ['name', 'code']

# Retrieve, Update, and Delete View for Herbarium
class HerbariumRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Herbarium.objects.all()
    serializer_class = HerbariumSerializer
