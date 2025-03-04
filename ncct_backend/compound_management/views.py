from rest_framework import viewsets
from .models import Compound
from .serializers import CompoundSerializer

class CompoundViewSet(viewsets.ModelViewSet):
    queryset = Compound.objects.all()
    serializer_class = CompoundSerializer