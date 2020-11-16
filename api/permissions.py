from rest_framework import permissions


class IsAdminPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_staff:
            return True

        if request.user.is_authenticated and request.user.role in ('admin', 'django_adm'):
            return True

        return False


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return(request.user.is_staff or \
            request.method in permissions.SAFE_METHODS or \
                (request.user.is_authenticated and request.user.role in ('admin', 'django_adm')))

        


class IsAuthorOrModeratorOrAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_authenticated:
            if request.user.role in ['moderator', 'admin'] or request.user == obj.author:
                return True

        return False
