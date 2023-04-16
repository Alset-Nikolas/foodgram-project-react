from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("api/", include("users.urls")),
    path("api/", include("recipes.urls")),
    path("api/", include("tags.urls")),
    path("api/", include("ingredients.urls")),
    path("admin/", admin.site.urls),
]
