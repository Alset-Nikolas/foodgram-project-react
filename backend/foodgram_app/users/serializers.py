from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.core.validators import validate_email
from django.shortcuts import get_object_or_404
from .models import Subscriptions
from recipes.serializers import MainRecipeSerializer

User = get_user_model()


class CastomAuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(write_only=True)
    password = serializers.CharField(trim_whitespace=False, write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = get_object_or_404(User, email=email)
            if not user:
                msg = "Unable to log in with provided credentials."
                raise serializers.ValidationError(msg, code="authorization")
            if not user.check_password(password):
                msg = "not valid password"
                raise serializers.ValidationError(msg, code="authorization")

        else:
            msg = 'Must include "email" and "password".'
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_current_password(self, current_password):
        user = self.context.get("user")
        if not user.check_password(current_password):
            raise serializers.ValidationError("Wrong password.", code=400)
        return current_password


class UserSubscriptionsSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    username = serializers.RegexField(
        regex=r"^[\w.@+-]+$",
        max_length=150,
        read_only=True,

    )
    recipes = MainRecipeSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "recipes",
        ]
        extra_kwargs = {
            "username": {"read_only": True},
            "email": {"read_only": True},
            "first_name": {"read_only": True},
            "last_name": {"read_only": True},
            "recipes": {"read_only": True},
        }

    def create(self, **data):
        return Subscriptions.objects.create(**data)

    def validate(self, data, **args):
        user = self.initial_data.get("user")
        author = self.initial_data.get("author")
        if user == author:
            raise serializers.ValidationError(
                {"err": "Нельзя на себя подписаться"}
            )
        if author in user.get_subscriptions():
            raise serializers.ValidationError({"err": "Уже подписаны"})
        return data
