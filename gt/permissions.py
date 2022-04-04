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
        token = request.data.get('recaptcha')
        if token:
            r = post(
                "https://recaptcha.google.cn/recaptcha/api/siteverify", {
                    'response': token,
                    'ip': request.ip,
                    'secret': settings.RECAPTCHA_SECRET,
                }).json()
            if not r['success']:
                raise AuthenticationFailed({
                    'status': 'error',
                    'detail': '人机验证出错, 请重试'
                })
            elif r['score'] < 0.6:
                raise AuthenticationFailed({
                    'status': 'error',
                    'detail': '您未能通过人机验证！'
                })
            else:
                return True


class RequireWeChat(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user and not request.user.wechat:
            raise AuthenticationFailed({
                'status': 'error',
                'detail': '该功能需要您绑定微信后使用！',
                'action': 'notice_wechat'
            })
        return True
