from django.shortcuts import render
from rest_framework import viewsets, mixins
from .models import Recipe, FavoriteRecipe
from .serializers import (
    ReadRecipeSerializer,
    WriteRecipeSerializer,
    ReadFavoriteRecipeSerializer,
    FavoriteRecipeSerializer,
)
from rest_framework import permissions
from .permissions import IsAuthorOrReadOnly
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404


# Create your views here.
class RecipeFavorite:
    def perform_create_favorite(self, serializer):
        serializer.create(
            user=self.request.user, recipe=self.request.data.get("recipe")
        )

    def get_object_favorite(self):
        return get_object_or_404(
            FavoriteRecipe,
            recipe=self.request.data.get("recipe"),
            user=self.request.user,
        )

    @action(
        detail=True,
        methods=["post", "delete"],
        permission_classes=[permissions.IsAuthenticated],
        url_path="favorite",
    )
    def user_add_favorite(self, request, pk):
        request.data["user"] = self.request.user
        request.data["recipe"] = get_object_or_404(Recipe, pk=pk)
        if self.request.method == "POST":
            self.perform_create = self.perform_create_favorite
            response = self.create(request)
            return (
                self.retrieve(request)
                if response.status_code == 200
                else response
            )
        self.get_object = self.get_object_favorite
        return self.destroy(request)


class RecipeViewSet(viewsets.ModelViewSet, RecipeFavorite):
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
        elif self.action == "user_add_favorite":
            if self.request.method == "POST":
                return ReadFavoriteRecipeSerializer
            return FavoriteRecipeSerializer
        return WriteRecipeSerializer
