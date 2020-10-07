from rest_framework.permissions import BasePermission


class IsStaffOrAdmin(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_staff:
            return True

        if request.user.is_authenticated:
            if request.user.role in ('admin', 'django_adm'):
                return True
