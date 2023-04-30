from django.contrib.auth import authenticate, get_user_model
from django.core.validators import validate_email
from django.shortcuts import get_object_or_404
from general_settings.serializers import UserSerializer
from rest_framework import serializers

from .models import Ingredients


class IngredientsSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Ingredients
        fields = [
            "id",
            "name",
            "measurement_unit",
        ]
