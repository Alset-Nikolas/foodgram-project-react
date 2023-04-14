from rest_framework import viewsets
from rest_framework import permissions
from django.contrib.auth import logout
from .serializers import (
    UserSerializer,
    CastomAuthTokenSerializer,
    ChangePasswordSerializer,
)
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics
from rest_framework import status
from rest_framework import viewsets, mixins
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    POST: Регистрация пользователя.
    GET: Список пользователей
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def get_instance(self):
        return self.request.user

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

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()


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
