from rest_framework.permissions import BasePermission, SAFE_METHODS


class ArticlePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.method in [
                'PUT', 'PATCH'
        ] and not (request.user == obj.author or request.user.is_staff):
            return False
        if not request.user.is_staff:
            for i in ["state"]:
                if request.data.get(i) is not None:
                    request.data.pop(i)
        return request.user.id == obj.id or request.user.is_staff or False


class CommentPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS or request.method == 'DELETE':
            return True
        else:
            return request.user.is_staff

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS or request.user.is_staff:
            return True
        elif request.method == 'DELETE':
            return request.user.id == obj.author.id
