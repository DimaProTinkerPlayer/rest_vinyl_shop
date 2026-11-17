from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthenticatedOrReadOnlyCustom(BasePermission):
    message = "Для виконання цієї дії необхідно увійти в систему."

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated)


class IsAdminOrReadOnly(BasePermission):
    message = "Доступ заборонено. Ця дія дозволена лише адміністраторам."

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)