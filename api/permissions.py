from rest_framework import permissions


class IsStaffOrAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_staff:
            return True

        if request.user.is_authenticated:
            if request.user.role in ('admin', 'django_adm'):
                return True

class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS or
            request.user.is_staff or
            request.user.is_authenticated and request.user.role in ('admin', 'django_adm')
        )