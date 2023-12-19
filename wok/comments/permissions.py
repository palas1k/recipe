from rest_framework.permissions import BasePermission, SAFE_METHODS

from comments.models import Comments


class IsOwnerOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj.author:
            return True

        return False
