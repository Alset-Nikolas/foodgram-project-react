from django.shortcuts import render
from rest_framework import mixins, permissions, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import Ingredients
from .serializers import IngredientsSerializer
from .filters import IngredientFilter

class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None
    filter_backends = [DjangoFilterBackend]
    filterset_class = IngredientFilter
