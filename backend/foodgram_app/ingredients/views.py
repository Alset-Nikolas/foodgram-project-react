from django.shortcuts import render
from rest_framework import mixins, permissions, viewsets

from .models import Ingredients
from .serializers import IngredientsSerializer


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None
    search_fields = ("name",)
