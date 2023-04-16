from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.core.validators import validate_email
from django.shortcuts import get_object_or_404
from .models import Ingredients
from users.serializers import UserSerializer


class IngredientsSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Ingredients
        fields = [
            "id",
            "name",
            "measurement_unit",
        ]


