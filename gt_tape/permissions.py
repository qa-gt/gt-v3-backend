from rest_framework.permissions import BasePermission, SAFE_METHODS


class TapeBoxPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS or request.method == 'POST':
            return True
        return obj.user == request.user or obj.user.is_staff