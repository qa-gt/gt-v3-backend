from rest_framework.authentication import BaseAuthentication

from ._jwt import jdecode
from gt_user.models import User


class GtAuthentication(BaseAuthentication):
    def authenticate(self, request):
        jwt = request.META.get('HTTP_AUTHORIZATION')
        if not jwt:
            return (None, None)
        jwt = jdecode(jwt)
        if jwt:
            return (User.objects.get(id=jwt['id']), None)
        else:
            return (None, None)
