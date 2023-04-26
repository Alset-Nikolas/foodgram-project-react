from django.db import models


# Create your models here.
class Ingredients(models.Model):
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    def __str__(self):
        return f"{self.name}"

    def get_recipe_amount(self, recipe):
        return self.ingredients_amount.filter(recipe=recipe).first().amount
