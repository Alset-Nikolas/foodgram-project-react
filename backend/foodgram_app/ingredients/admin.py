from django.contrib import admin

# Register your models here.
from .models import Ingredients


class IngredientsAdmin(admin.ModelAdmin):
    list_filter = ["name", "measurement_unit"]
    list_display = ("name",)


admin.site.register(Ingredients)
