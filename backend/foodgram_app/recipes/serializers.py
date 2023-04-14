from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.core.validators import validate_email
from django.shortcuts import get_object_or_404
from .models import Recipe
from users.serializers import UserSerializer


class RecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    author = UserSerializer(read_only=True)

    def validate_cooking_time(self, cooking_time):
        if cooking_time < 1:
            raise serializers.ValidationError("cooking_time >= 1")
        return super().validate(cooking_time)

    class Meta:
        model = Recipe
        fields = [
            "id",
            "author",
            "image",
            "name",
            "text",
            "cooking_time",
        ]
