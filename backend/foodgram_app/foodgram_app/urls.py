from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("api/", include("users.urls")),
    path("api/", include("recipes.urls")),
    path("api/", include("tags.urls")),
    path("api/", include("ingredients.urls")),
    path("api/admin/", admin.site.urls),
]
