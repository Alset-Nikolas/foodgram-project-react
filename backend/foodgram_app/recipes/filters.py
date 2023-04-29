from django_filters.rest_framework import FilterSet, CharFilter, BooleanFilter
from .models import Recipe
from django.db.models import QuerySet


class RecipeFilter(FilterSet):
    tags = CharFilter(field_name="tags__slug", method="filter_tags")
    is_in_shopping_cart = BooleanFilter(method="filter_is_in_shopping_cart")

    def __init__(
        self, data=None, queryset=None, *, request=None, prefix=None, **kwargs
    ):
        self.user = request.user
        super().__init__(data, queryset, request=request, prefix=prefix)

    def filter_tags(self, queryset, name, tags):
        assert False, tags
        return queryset.filter(tags__name__contains=tags.split(","))

    def filter_is_in_shopping_cart(
        self, queryset: QuerySet, name: str, is_in_shopping_cart: bool
    ):
        if not self.user.is_authenticated or not is_in_shopping_cart:
            return queryset

        return queryset.filter(users_shopping__user=self.user)

    class Meta:
        model = Recipe
        fields = ["tags", "is_in_shopping_cart"]
