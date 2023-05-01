from django_filters.rest_framework import (
    FilterSet,
    CharFilter,
)

from .models import Ingredients


class IngredientFilter(FilterSet):
    name = CharFilter(field_name="name", method="filter_name")

    def filter_name(
        self, queryset, name_: str, name: str
    ):
        return queryset.filter(name__icontains=name)
    class Meta:
        model = Ingredients
        fields = ["name"]
