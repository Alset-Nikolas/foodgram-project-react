from django.db import models
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from tags.models import Tags
from ingredients.models import Ingredients

User = get_user_model()


# Create your models here.
class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="автор",
    )
    image = models.ImageField(upload_to="recipes/")
    name = models.CharField(max_length=200)
    text = models.TextField()
    cooking_time = models.IntegerField()

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
    amount = models.IntegerField()

    class Meta:
        verbose_name = "связь рецепт-ингредиента"
        verbose_name_plural = "связи рецепт-ингредиента"

    def __str__(self):
        return f"{self.recipe.name} ({self.ingredient.name} {self.amount})"
