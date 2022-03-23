from rest_framework.permissions import BasePermission, SAFE_METHODS


class UserPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if not request.user or not (request.user.id == obj.id
                                    or request.user.is_staff):
            return False
        if request.user and not request.user.is_staff:
            for i in ["ban_state", "tags"]:
                if request.data.get(i) is not None:
                    request.data.pop(i)
        if request.user and not request.user.is_superuser:
            for i in ["is_staff", "is_superuser"]:
                if request.data.get(i) is not None:
                    request.data.pop(i)
        return True
