import jwt
from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from rest_framework.exceptions import AuthenticationFailed


def jencode(payload, expire_time=0):
    if payload.get('exp') is None:
        payload['exp'] = timezone.now() + timedelta(seconds=int(expire_time))
    jwt_data = jwt.encode(payload=payload,
                          key=settings.SECRET_KEY,
                          algorithm='HS256')
    if type(jwt_data) is bytes:
        jwt_data = jwt_data.decode('utf-8')
    return f'{settings.JWT_PREFIX} {jwt_data}'


def jdecode(token, raise_error=True):
    try:
        return jwt.decode(jwt=token,
                          key=settings.SECRET_KEY,
                          leeway=settings.JWT_EXPIRE_TIME,
                          algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        if raise_error:
            raise AuthenticationFailed({
                'status': 'error',
                'action': 'relogin',
                'detail': '登录信息已过期, 请重新登录'
            })
        else:
            return None
    # except Exception as e:
    # print(e)
    # return None


if __name__ == '__main__':
    print(jdecode(jencode({'username': 'admin'})))
