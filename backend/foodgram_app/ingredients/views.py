from django.shortcuts import render
from rest_framework import permissions
from rest_framework import viewsets, mixins

from .models import Ingredients
from .serializers import IngredientsSerializer


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None
    search_fields = ("name",)
