# backend/ncct_backend/compound_management/serializers.py
from rest_framework import serializers
from .models import Compound

class CompoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compound
        fields = '__all__'