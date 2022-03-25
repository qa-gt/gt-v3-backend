from django.conf import settings
from requests import post
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class NoEdit(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS or request.method in [
                'POST', 'DELETE'
        ] or (request.user and request.user.is_staff):
            return True


class RobotCheck(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        v_server = request.data.get('server')
        v_token = request.data.get('token')
        v_scene = request.data.get('scene') and int(request.data['scene']) or 0
        if v_server and v_token:
            r = post(
                v_server, {
                    'token': v_token,
                    'ip': request.ip,
                    'id': settings.VAPTCHA_VID,
                    'secretkey': settings.VAPTCHA_KEY,
                    'scene': v_scene
                }).json()
            print(r)
            if not r['success']:
                raise AuthenticationFailed({
                    'status': 'error',
                    'action': 'rerobot',
                    'detail': '人机验证出错, 请重试'
                })
            else:
                return True
