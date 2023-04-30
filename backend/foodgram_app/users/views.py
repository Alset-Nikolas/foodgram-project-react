from django.contrib.auth import get_user_model, logout
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from general_settings.serializers import UserSerializer
from rest_framework import generics, mixins, permissions, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Subscriptions
from .serializers import (CastomAuthTokenSerializer, ChangePasswordSerializer,
                          UserSubscriptionsSerializer)

User = get_user_model()


class UserViewSetSubscribeBase:
    def get_queryset_subscribe(self):
        return self.request.user.get_subscriptions()

    def get_subscribe_object(self):
        return get_object_or_404(
            Subscriptions,
            author=self.request.data.get("author"),
            user=self.request.user,
        )

    def perform_create_subscribe(self, serializer):
        serializer.create(
            user=self.request.user, author=self.request.data.get("author")
        )

    @action(
        detail=False,
        methods=["get"],
        serializer_class=UserSubscriptionsSerializer,
        permission_classes=[permissions.IsAuthenticated],
        url_path="subscriptions",
    )
    def user_subscriptions(self, request):
        self.get_queryset = self.get_queryset_subscribe
        return self.list(request)

    @action(
        detail=True,
        methods=["post", "delete"],
        serializer_class=UserSubscriptionsSerializer,
        permission_classes=[permissions.IsAuthenticated],
        url_path="subscribe",
    )
    def user_update_subscription(self, request, pk):
        self.get_queryset = self.get_queryset_subscribe
        request.data["author"] = get_object_or_404(User, pk=pk)
        request.data["user"] = self.get_instance()
        if request.method == "POST":
            self.perform_create = self.perform_create_subscribe
            response = self.create(request)
            if response.status_code == 201:
                return self.list(request)
            return response

        self.get_object = self.get_subscribe_object
        return self.destroy(request)


class UserViewSet(viewsets.ModelViewSet, UserViewSetSubscribeBase):
    """
    POST: Регистрация пользователя.
    GET: Список пользователей
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def get_instance(self):
        return self.request.user

    def get_context__subscribe(self, *args, **kwargs):
        context = super().get_serializer_context()
        context["user"] = self.request.user
        context["author"] = self.request.data.get("author")
        return context

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()

    @action(
        detail=False,
        methods=["get"],
        serializer_class=UserSerializer,
        permission_classes=[permissions.IsAuthenticated],
        url_path="me",
    )
    def user_profile(self, request):
        self.get_object = self.get_instance
        return self.retrieve(request)


class CustomAuthToken(ObtainAuthToken):
    serializer_class = CastomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"auth_token": token.key})


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def user_logout(request):
    request.user.auth_token.delete()

    logout(request)

    return Response(status=status.HTTP_204_NO_CONTENT)


class ChangePasswordViewSet(APIView):
    model = User
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CastomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        user = self.request.user
        serializer = ChangePasswordSerializer(
            data=request.data, context={"user": user}
        )
        if serializer.is_valid():
            user.password = make_password(serializer.data.get("new_password"))
            user.save()

            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
