from django.db import models
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from tags.models import Tags
from ingredients.models import Ingredients
import typing as t
from django.core.exceptions import ValidationError

User = get_user_model()


def user_directory_path(instance, filename):
    return "recipes/{0}".format(filename)


def validate_range(value):
    if value < 1:
        raise ValidationError("cooking_time > 1 ")


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="автор",
    )
    image = models.ImageField(upload_to=user_directory_path)
    name = models.CharField(max_length=200)
    text = models.TextField()
    cooking_time = models.IntegerField(validators=[validate_range])

    tags = models.ManyToManyField(
        Tags, through="RecipeTags", verbose_name="Теги"
    )

    ingredients = models.ManyToManyField(
        Ingredients, through="RecipeIngredients", verbose_name="Ингредиенты"
    )

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return f"{self.name}"

    def get_ingredients(self):
        return self.ingredients.all()


class RecipeTags(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name="рецепт",
    )
    tag = models.ForeignKey(
        Tags,
        on_delete=models.CASCADE,
        verbose_name="тег",
    )

    class Meta:
        verbose_name = "связь рецепт-тег"
        verbose_name_plural = "связи рецепт-теги"

    def __str__(self):
        return f"{self.tag} {self.recipe}"


class RecipeIngredients(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name="рецепт",
    )
    ingredient = models.ForeignKey(
        Ingredients,
        on_delete=models.CASCADE,
        verbose_name="ингредиент",
        related_name="ingredients_amount",
    )
    amount = models.IntegerField(validators=[validate_range])

    class Meta:
        verbose_name = "связь рецепт-ингредиента"
        verbose_name_plural = "связи рецепт-ингредиента"

    def __str__(self):
        return f"{self.recipe.name} ({self.ingredient.name} {self.amount})"


class FavoriteRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name="рецепт",
        related_name="users_favorites",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favorites",
        verbose_name="пользователь",
    )

    class Meta:
        verbose_name = "Избранные рецепты"
        verbose_name_plural = "Избранный рецепт"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"], name="unique favorits"
            )
        ]


class ShoppingRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name="рецепт",
        related_name="users_shopping",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="shopping",
        verbose_name="пользователь",
    )

    class Meta:
        verbose_name = "Покупки"
        verbose_name_plural = "Покупка"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"], name="unique shopping"
            )
        ]
