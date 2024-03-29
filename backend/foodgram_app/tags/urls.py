from django.urls import include, path
from rest_framework import routers

from .views import TagsViewSet

router = routers.DefaultRouter()
router.register(r"tags", TagsViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
