from django.db.models import QuerySet
from django_filters.rest_framework import (
    BooleanFilter,
    AllValuesMultipleFilter,
    FilterSet,
)

from .models import Recipe


class RecipeFilter(FilterSet):
    tags = AllValuesMultipleFilter(field_name="tags__slug")
    is_in_shopping_cart = BooleanFilter(method="filter_is_in_shopping_cart")

    def __init__(
        self, data=None, queryset=None, *, request=None, prefix=None, **kwargs
    ):
        self.user = request.user
        super().__init__(data, queryset, request=request, prefix=prefix)

    def filter_is_in_shopping_cart(
        self, queryset: QuerySet, name: str, is_in_shopping_cart: bool
    ):
        if not self.user.is_authenticated or not is_in_shopping_cart:
            return queryset

        return queryset.filter(users_shopping__user=self.user)

    class Meta:
        model = Recipe
        fields = ["tags", "is_in_shopping_cart"]
