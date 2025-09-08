from rest_framework import serializers
from .models import Reference


class ReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reference
        fields = '__all__'

    def validate(self, data):
        """
        Check for duplicate references.
        """
        doi = data.get('doi')
        title = data.get('title')
        author = data.get('author')

        if doi:
            if Reference.objects.filter(doi=doi).exists():
                raise serializers.ValidationError("A reference with this DOI already exists.")
        elif title and author:
            if Reference.objects.filter(title=title, author=author).exists():
                raise serializers.ValidationError("A reference with this title and author already exists.")

        return data

