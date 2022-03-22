from rest_framework.permissions import BasePermission


class UserPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        if request.user and not request.user.state >= 1:
            for i in ["state", "tags"]:
                if request.data.get(i) is not None:
                    request.data.pop(i)
        return request.user and (request.user.id == obj.id
                                 or request.user.state >= 1) or False
