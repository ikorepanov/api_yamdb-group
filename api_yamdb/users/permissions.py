from rest_framework import permissions


class IsAdminOrSuperUser(permissions.BasePermission):
    '''Разрешение для администратора и суперпользователя'''
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and (
                request.user.is_admin
                or request.user.is_staff
                or request.user.is_superuser))
