from django.contrib import admin

# Register your models here.
from .models import Recipe, RecipeTags, RecipeIngredients

admin.site.register(Recipe)
admin.site.register(RecipeTags)
admin.site.register(RecipeIngredients)
