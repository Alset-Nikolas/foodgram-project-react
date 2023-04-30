from django.contrib import admin

# Register your models here.
from .models import (FavoriteRecipe, Recipe, RecipeIngredients, RecipeTags,
                     ShoppingRecipe)


class RecipeAdmin(admin.ModelAdmin):
    list_filter = ["author", "name", "tags"]
    list_display = ("author", "name", "number_additions")

    def number_additions(self, obj):
        return len(FavoriteRecipe.objects.filter(recipe=obj).all())


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeTags)
admin.site.register(RecipeIngredients)
admin.site.register(ShoppingRecipe)
admin.site.register(FavoriteRecipe)
