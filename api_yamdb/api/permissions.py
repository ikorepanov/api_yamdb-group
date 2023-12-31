from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Безопасные методы запросов для всех. Остальные только
    аунтифицированным пользователям с правами админа."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_admin
        )


class IsAdminOrSuperUser(permissions.BasePermission):
    '''Разрешение для администратора и суперпользователя'''
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and (
                request.user.is_admin
                or request.user.is_staff
                or request.user.is_superuser))
