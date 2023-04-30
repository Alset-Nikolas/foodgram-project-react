from django.shortcuts import render
from rest_framework import permissions, viewsets

from .models import Tags
from .serializers import TagSerializer


# Create your views here.
class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None
