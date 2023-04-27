from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.core.validators import validate_email
from django.shortcuts import get_object_or_404
from .models import Recipe, RecipeIngredients, FavoriteRecipe, ShoppingRecipe
from tags.models import Tags
from tags.serializers import TagSerializer
from ingredients.models import Ingredients
from general_settings.serializers import UserSerializer
from drf_extra_fields.fields import Base64ImageField


User = get_user_model()


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
    is_favorited = serializers.SerializerMethodField(
        read_only=True,
    )
    is_in_shopping_cart = serializers.SerializerMethodField(
        read_only=True,
    )

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
            "is_favorited",
            "is_in_shopping_cart",
        ]

    def validate_cooking_time(self, cooking_time):
        if cooking_time < 1:
            raise serializers.ValidationError("cooking_time >= 1")
        return super().validate(cooking_time)

    def get_is_favorited(self, recipe):
        request = self.context.get("request")
        if not request:
            return False
        user = request.user
        return (
            FavoriteRecipe.objects.filter(user=user, recipe=recipe).exists()
            if user.is_authenticated
            else False
        )

    def get_is_in_shopping_cart(self, recipe):
        request = self.context.get("request")
        if not request:
            return False
        user = request.user
        return (
            ShoppingRecipe.objects.filter(user=user, recipe=recipe).exists()
            if user.is_authenticated
            else False
        )

    def to_representation(self, instance):
        data = super(ReadRecipeSerializer, self).to_representation(instance)
        image_path = str(data.get("image")).replace(":8000", "")
        image_path = image_path.replace("/media", "/api/media")
        data["image"] = image_path
        return data


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
        items = [
            RecipeIngredients(
                recipe=instance,
                ingredient=Ingredients.objects.get(
                    pk=info_ingredient.get("ingredient").get("id")
                ),
                amount=info_ingredient.get("amount"),
            )
            for info_ingredient in ingredients_info
        ]
        RecipeIngredients.objects.bulk_create(items)

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


class MainRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    image = Base64ImageField(
        max_length=None,
        use_url=True,
        read_only=True,
    )

    def validate_cooking_time(self, cooking_time):
        if cooking_time < 1:
            raise serializers.ValidationError("cooking_time >= 1")
        return super().validate(cooking_time)

    class Meta:
        model = Recipe
        fields = [
            "id",
            "name",
            "image",
            "cooking_time",
        ]


class ReadFavoriteRecipeSerializer(MainRecipeSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Recipe
        fields = [
            "id",
            "name",
            "image",
            "cooking_time",
        ]
        extra_kwargs = {
            "name": {"read_only": True},
            "image": {"read_only": True},
            "cooking_time": {"read_only": True},
        }

    def create(self, **kwargs):
        return FavoriteRecipe.objects.create(**kwargs)

    def validate(self, data, **args):
        user = self.initial_data.get("user")
        recipe = self.initial_data.get("recipe")
        if recipe in user.get_favorites():
            raise serializers.ValidationError({"err": "Уже в избранном!"})
        return data


class FavoriteRecipeSerializer(MainRecipeSerializer):
    class Meta:
        model = Recipe
        fields = [
            "id",
            "name",
            "image",
            "cooking_time",
        ]
        extra_kwargs = {
            "name": {"read_only": True},
            "image": {"read_only": True},
            "cooking_time": {"read_only": True},
        }


class ShoppingRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = ShoppingRecipe
        fields = [
            "id",
        ]


class ReadShoppingRecipeSerializer(MainRecipeSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Recipe
        fields = [
            "id",
            "name",
            "image",
            "cooking_time",
        ]
        extra_kwargs = {
            "name": {"read_only": True},
            "image": {"read_only": True},
            "cooking_time": {"read_only": True},
        }

    def create(self, **kwargs):
        return ShoppingRecipe.objects.create(**kwargs)

    def validate(self, data, **args):
        user = self.initial_data.get("user")
        recipe = self.initial_data.get("recipe")
        if recipe in user.get_shopping():
            raise serializers.ValidationError(
                {"err": "Такой рецепт уже добавлен"}
            )
        return data
