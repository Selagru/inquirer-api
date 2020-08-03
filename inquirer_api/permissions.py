from rest_framework import permissions, filters
from django.core.exceptions import FieldError


class IsAdminUserOrReadOnly(permissions.BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return bool(request.method in permissions.SAFE_METHODS or request.user and request.user.is_staff)


class IsOwnerFilterBackend(filters.BaseFilterBackend):
    """
    Фильтр, который позволят пользователю видеть и редактировать только собственные объекты.
    """
    def filter_queryset(self, request, queryset, view):
        if request.user.is_anonymous:
            return queryset.filter(session_key=request.session.session_key)
        try:
            response = queryset.filter(owner=request.user)
        except FieldError:
            response = queryset.filter(user=request.user)
        return response


class ReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS
