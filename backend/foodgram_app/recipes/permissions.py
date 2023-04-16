from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        if view.action == "retrieve" or obj.author == request.user:
            return True
        if request.user.is_staff:
            return True
        return False
