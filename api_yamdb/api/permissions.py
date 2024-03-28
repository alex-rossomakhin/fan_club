from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Доступ только для администраторов и суперюзеров
    (модели регистрации и управления юзерами)."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin
            or request.user.is_superuser
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """Доступ на изменение только для администраторов
    (модели жанров, категорий и тайтлов)."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            request.user.is_authenticated
            and request.user.is_admin
            or request.user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            request.user.is_authenticated
            and request.user.is_admin
            or request.user.is_superuser
        )


class IsAuthorStaffOrReadOnly(permissions.BasePermission):
    """Доступ на изменение только для авторов и персонала сайта
    (модели коментов и отзывов)."""

    message = 'Изменения доступны только авторам или модераторам!'

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            obj.author == request.user
            or request.user.is_moderator
            or request.user.is_admin
        )
