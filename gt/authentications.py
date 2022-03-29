from django.conf import settings
from gt_user.models import User
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import SAFE_METHODS

from ._jwt import jdecode


class GtAuthentication(BaseAuthentication):
    def authenticate(self, request):
        jwt = request.META.get('HTTP_AUTHORIZATION')
        if not jwt:
            return (None, None)
        jwt = str(jwt).split(maxsplit=1)
        if jwt[0] != settings.JWT_PREFIX:
            raise AuthenticationFailed({
                'status': 'error',
                'action': 'relogin',
                'detail': 'Token 异常'
            })
        jwt = jwt[1]
        raise_error = request.method not in SAFE_METHODS
        user = jdecode(jwt, raise_error)
        if user:
            user = User.objects.filter(id=user['id'])
            if user.exists() and user.first().is_active:
                return (user.first(), jwt)
            else:
                return (None, None)
        else:
            return (None, None)
