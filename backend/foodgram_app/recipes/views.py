import typing as t

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django_filters.rest_framework import DjangoFilterBackend
from reportlab.pdfgen import canvas
from rest_framework import mixins, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import RecipeFilter
from .models import FavoriteRecipe, Recipe, ShoppingRecipe
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    FavoriteRecipeSerializer,
    MainRecipeSerializer,
    ReadFavoriteRecipeSerializer,
    ReadRecipeSerializer,
    ReadShoppingRecipeSerializer,
    ShoppingRecipeSerializer,
    WriteRecipeSerializer,
)


class RecipeBaseManager:
    def get_object_recipe(self):
        return self.request.data.get("recipe")

    def user_add_option(self, request, pk):
        request.data["user"] = self.request.user
        request.data["recipe"] = get_object_or_404(Recipe, pk=pk)
        if self.request.method == "POST":
            response = self.create(request)
            if response.status_code >= 200 and response.status_code < 300:
                self.get_object = self.get_object_recipe
                instance = self.get_object()
                serializer = self.get_serializer(instance)
                return Response(serializer.data, 201)
            return response
        return self.destroy(request)


class RecipeShopping(RecipeBaseManager):
    def perform_create_shopping(self, serializer):
        serializer.create(
            user=self.request.user, recipe=self.request.data.get("recipe")
        )

    def get_object_shopping(self):
        return get_object_or_404(
            ShoppingRecipe,
            recipe=self.request.data.get("recipe"),
            user=self.request.user,
        )

    @action(
        detail=True,
        methods=["post", "delete"],
        permission_classes=[permissions.IsAuthenticated],
        url_path="shopping_cart",
    )
    def user_shopping(self, request, pk):
        self.perform_create = self.perform_create_shopping
        self.get_object = self.get_object_shopping
        return self.user_add_option(request, pk)

    def __getuser_ingredients_info(self, request):
        info = dict()
        for rec in request.user.get_shopping():
            for ing in rec.get_ingredients():
                if ing.name not in info:
                    info[ing.name] = {
                        "measurement_unit": ing.measurement_unit,
                        "amount": 0,
                    }
                info[ing.name]["amount"] += ing.get_recipe_amount(rec)
        return info.items()

    def __create_pdf(self, request):
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="file.pdf"'
        p = canvas.Canvas(response)
        p.setFont("DejaVuSerif", 25)

        row = 0
        for name, info_inredient in self.__getuser_ingredients_info(request):
            text = f'{name} ({info_inredient["measurement_unit"]}): {info_inredient.get("amount")}'
            p.drawString(80, 700 + 10 * row, text)
            row += 1

        p.showPage()
        p.save()
        return response

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[permissions.IsAuthenticated],
        url_path="download_shopping_cart",
    )
    def download_shopping_cart(self, request):
        return self.__create_pdf(request)


class RecipeFavorite(RecipeBaseManager):
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
    def user_favorite(self, request, pk):
        self.perform_create = self.perform_create_favorite
        self.get_object = self.get_object_favorite
        return self.user_add_option(request, pk)


class RecipeViewSet(viewsets.ModelViewSet, RecipeFavorite, RecipeShopping):
    """
    POST: Создание рецепта
    GET: Список рецептов
    """

    queryset = Recipe.objects.all()
    serializer_class = ReadRecipeSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly,
    ]
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return ReadRecipeSerializer
        elif self.action == "user_favorite":
            return ReadFavoriteRecipeSerializer

        elif self.action == "user_shopping":
            if self.request.method == "DELETE":
                return ShoppingRecipeSerializer
            return ReadShoppingRecipeSerializer
        elif self.action == "download_shopping_cart":
            return ReadRecipeSerializer

        return WriteRecipeSerializer
