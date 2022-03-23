import jwt
from django.conf import settings
from django.utils import timezone
from rest_framework.exceptions import AuthenticationFailed


def jencode(payload):
    if payload.get('exp') is None:
        payload['exp'] = timezone.now()
    jwt_data = jwt.encode(payload=payload,
                          key=settings.SECRET_KEY,
                          algorithm='HS256')
    return f'{settings.JWT_PREFIX} {jwt_data}'


def jdecode(token):
    try:
        return jwt.decode(jwt=token,
                          key=settings.SECRET_KEY,
                          leeway=settings.JWT_EXPIRE_TIME,
                          algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed({
            'status': 'error',
            'action': 'relogin',
            'detail': '登录信息已过期, 请重新登录'
        })
    # except Exception as e:
    # print(e)
    # return None


if __name__ == '__main__':
    print(jdecode(jencode({'username': 'admin'})))
