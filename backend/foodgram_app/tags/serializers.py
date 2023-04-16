from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.core.validators import validate_email
from django.shortcuts import get_object_or_404
from .models import Tags
from users.serializers import UserSerializer


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
