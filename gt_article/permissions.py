from rest_framework.permissions import BasePermission, SAFE_METHODS


class ArticlePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if not request.user:
            return False
        if request.method in [
                'PUT', 'PATCH'
        ] and not (request.user == obj.author or request.user.is_staff):
            return False
        if request.user and not request.user.is_staff:
            for i in ["ban_state"]:
                if request.data.get(i) is not None:
                    request.data.pop(i)
        return request.user and (request.user.id == obj.id
                                 or request.user.is_staff) or False
