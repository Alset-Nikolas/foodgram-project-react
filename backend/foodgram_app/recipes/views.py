from django.shortcuts import render
from rest_framework import viewsets, mixins
from .models import Recipe
from .serializers import ReadRecipeSerializer, WriteRecipeSerializer
from rest_framework import permissions
from .permissions import IsAuthorOrReadOnly


# Create your views here.
class RecipeViewSet(viewsets.ModelViewSet):
    """
    POST: Создание рецепта
    GET: Список рецептов
    """

    queryset = Recipe.objects.all()
    serializer_class = ReadRecipeSerializer
    permission_classes = [permissions.AllowAny]
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly,
    ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return ReadRecipeSerializer
        return WriteRecipeSerializer
