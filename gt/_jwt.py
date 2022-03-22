import jwt
from django.conf import settings


def jencode(payload):
    jwt_data = jwt.encode(
        payload=payload, key=settings.SECRET_KEY, algorithm="HS256")
    return f"{settings.JWT_PREFIX} {jwt_data}"


def jdecode(token):
    try:
        return jwt.decode(jwt=token,
                          key=settings.SECRET_KEY,
                          leeway=settings.JWT_EXPIRE_TIME,
                          algorithms=["HS256"])
    except Exception as e:
        print(e)
        return None


if __name__ == "__main__":
    print(jdecode(jencode({"username": "admin"})))
