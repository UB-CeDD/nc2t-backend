# ncct_backend/compound_management/views.py
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Compound
from .serializers import CompoundSerializer


# List and Create View
class CompoundListCreateView(ListCreateAPIView):
    queryset = Compound.objects.all()
    serializer_class = CompoundSerializer

    def get_permissions(self):
        if self.request.method in ['GET', 'HEAD', 'OPTIONS']:
            return [AllowAny()]
        return [IsAuthenticated()]

# Retrieve, Update, and Destroy View
class CompoundRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Compound.objects.all()
    serializer_class = CompoundSerializer

    def get_permissions(self):
        if self.request.method in ['GET', 'HEAD', 'OPTIONS']:
            return [AllowAny()]
        return [IsAuthenticated()]
