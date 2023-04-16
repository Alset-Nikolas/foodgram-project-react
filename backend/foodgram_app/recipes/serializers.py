from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.core.validators import validate_email
from django.shortcuts import get_object_or_404
from .models import Recipe, RecipeIngredients
from tags.models import Tags
from users.serializers import UserSerializer
from tags.serializers import TagSerializer
from ingredients.models import Ingredients


class Base64ImageField(serializers.ImageField):
    """
    A Django REST framework field for handling image-uploads through raw post data.
    It uses base64 for encoding and decoding the contents of the file.

    Heavily based on
    https://github.com/tomchristie/django-rest-framework/pull/1268

    Updated for Django REST framework 3.
    """

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if "data:" in data and ";base64," in data:
                # Break out the header from the base64 content
                header, data = data.split(";base64,")

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail("invalid_image")

            # Generate file name:
            file_name = str(uuid.uuid4())[
                :12
            ]  # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (
                file_name,
                file_extension,
            )

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension


class RecipeIngredientsReadSerilizer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="ingredient.id")
    name = serializers.ReadOnlyField(source="ingredient.name")
    measurement_unit = serializers.ReadOnlyField(
        source="ingredient.measurement_unit"
    )

    class Meta:
        model = RecipeIngredients
        fields = ["id", "name", "measurement_unit", "amount"]


class RecipeIngredientWriteSerilizer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="ingredient.id")

    class Meta:
        model = RecipeIngredients
        fields = ["id", "amount"]


class ReadRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    author = UserSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)
    ingredients = RecipeIngredientsReadSerilizer(
        source="recipeingredients_set", many=True
    )
    image = Base64ImageField(
        max_length=None,
        use_url=True,
    )

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
            "tags",
            "ingredients",
        ]


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = "__all__"


class WriteRecipeSerializer(ReadRecipeSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tags.objects.all(), many=True
    )
    ingredients = RecipeIngredientWriteSerilizer(
        many=True, source="recipeingredients_set"
    )

    def __create_tags_and_ingredients(self, instance, tags, ingredients_info):
        [instance.tags.add(tag) for tag in tags]
        instance.save()
        for info_ingredient in ingredients_info:
            RecipeIngredients.objects.create(
                recipe=instance,
                ingredient=Ingredients.objects.get(
                    pk=info_ingredient.get("ingredient").get("id")
                ),
                amount=info_ingredient.get("amount"),
            )

    def create(self, validated_data):
        ingredients_info = validated_data.pop("recipeingredients_set")
        tags = validated_data.pop("tags")
        instance = Recipe.objects.create(**validated_data)
        self.__create_tags_and_ingredients(instance, tags, ingredients_info)
        return instance

    def update(self, instance, validated_data):
        ingredients_info = validated_data.pop("recipeingredients_set")
        tags = validated_data.pop("tags")
        instance = super().update(instance, validated_data)
        instance.tags.clear()
        instance.ingredients.clear()
        self.__create_tags_and_ingredients(instance, tags, ingredients_info)
        return instance

    def to_representation(self, instance):
        serializer = ReadRecipeSerializer(instance)
        return serializer.data
