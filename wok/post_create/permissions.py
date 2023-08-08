from rest_framework.permissions import BasePermission
from rest_framework import permissions


class IsAdminAuthenticatedReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and (request.method in permissions.SAFE_METHODS or request.method == 'DELETE'):
            return True
        return bool(request.user.is_staff)


class IsAdminOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST' and request.user.is_staff:
            return True
        return False
