from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

from .models import Compound
from .serializers import CompoundSerializer


# List and Create View
class CompoundListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Compound.objects.all()
    serializer_class = CompoundSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['subclass', 'compound_class', 'smiles']


# Retrieve, Update, and Delete View
class CompoundRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Compound.objects.all()
    serializer_class = CompoundSerializer
