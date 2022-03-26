from rest_framework.permissions import BasePermission, SAFE_METHODS


class ArticlePermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.ban_state > -1

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if not (request.user == obj.author or request.user.is_staff):
            return False
        if not request.user.is_staff:
            for i in ["state"]:
                if request.data.get(i) is not None:
                    request.data.pop(i)
        return True


class CommentPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.ban_state > -2

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS or request.user.is_staff:
            return True
        return request.user.id == obj.author.id


class CollectPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        print(123)
        return request.method in SAFE_METHODS or request.user.id == obj.user.id
