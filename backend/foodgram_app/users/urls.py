from django.urls import include, path
from rest_framework import routers
from .views import (
    UserViewSet,
    CustomAuthToken,
    user_logout,
    ChangePasswordViewSet,
)

router = routers.DefaultRouter()
router.register(r"users", UserViewSet)

urlpatterns = [
    path("auth/token/login/", CustomAuthToken.as_view()),
    path(
        "auth/token/logout/",
        user_logout,
    ),
    path(
        "users/set_password/",
        ChangePasswordViewSet.as_view(),
    ),
    path("", include(router.urls)),
]
