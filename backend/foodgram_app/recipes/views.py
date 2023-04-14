from django.shortcuts import render
from rest_framework import viewsets, mixins
from .models import Recipe
from .serializers import RecipeSerializer
from rest_framework import permissions


# Create your views here.
class RecipeViewSet(viewsets.ModelViewSet):
    """
    POST: Создание рецепта
    GET: Список рецептов
    """

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.AllowAny]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
