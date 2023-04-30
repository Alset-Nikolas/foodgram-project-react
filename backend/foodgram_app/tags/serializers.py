from rest_framework import serializers

from .models import Tags


class TagSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    color = serializers.RegexField(
        regex=r"^#(?:[0-9a-fA-F]{3}){1,2}$", max_length=7
    )

    class Meta:
        model = Tags
        fields = [
            "id",
            "name",
            "slug",
            "color",
        ]
