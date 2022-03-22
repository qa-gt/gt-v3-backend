from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import ValidationError
from django.conf import settings
from ._jwt import jdecode
from gt_user.models import User


class GtAuthentication(BaseAuthentication):
    def authenticate(self, request):
        jwt = request.META.get('HTTP_AUTHORIZATION')
        if not jwt:
            return None
        jwt = str(jwt).split(maxsplit=1)
        if jwt[0] != settings.JWT_PREFIX:
            raise ValidationError({'detail': 'Token 异常'})
        jwt = jwt[1]
        user = jdecode(jwt)
        if user:
            return (User.objects.get(id=user['id']), jwt)
        else:
            return (None, None)
