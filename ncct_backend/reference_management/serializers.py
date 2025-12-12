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

        # Exclude the current instance when validating duplicates during updates
        qs = Reference.objects.all()
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)

        if doi:
            if qs.filter(doi=doi).exists():
                raise serializers.ValidationError("A reference with this DOI already exists.")
        elif title and author:
            if qs.filter(title=title, author=author).exists():
                raise serializers.ValidationError("A reference with this title and author already exists.")

        return data

