from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser


class IsAdminOrStaff(BasePermission):
    def has_permission(self, request, view):
        return request.user and (
            request.user.is_superuser or request.user.is_staff
        )


class ReadOnlyForAll(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS
