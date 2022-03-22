from rest_framework.permissions import BasePermission


class NoDelete(BasePermission):
    def has_permission(self, request, view):
        return request.method != 'DELETE'
