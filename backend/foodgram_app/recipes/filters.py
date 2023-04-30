from django.db.models import QuerySet
from django_filters.rest_framework import (
    BooleanFilter,
    AllValuesMultipleFilter,
    FilterSet,
    CharFilter,
)

from .models import Recipe


class RecipeFilter(FilterSet):
    tags = AllValuesMultipleFilter(field_name="tags__slug")
    is_in_shopping_cart = BooleanFilter(method="filter_is_in_shopping_cart")
    is_favorited = BooleanFilter(method="filter_is_favorited")
    author = CharFilter(field_name="author")

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

    def filter_is_favorited(
        self, queryset: QuerySet, name: str, is_favorited: bool
    ):
        if not self.user.is_authenticated or not is_favorited:
            return queryset

        return queryset.filter(users_favorites__user=self.user)

    class Meta:
        model = Recipe
        fields = ["tags", "is_in_shopping_cart"]
