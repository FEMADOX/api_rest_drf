from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS
            or request.user and request.user.is_staff
        )


class IsClientOrAdmin(BasePermission):
    def has_permission(self, request, view):
        client_id = view.kwargs.get("client_id")
        return bool(
            request.user.is_authenticated
            and request.user.id == client_id
            or request.user.is_staff
        )
