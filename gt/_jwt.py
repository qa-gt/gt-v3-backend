import datetime

import jwt

from .settings import SECRET_KEY


def jencode(payload):
    return jwt.encode(payload=payload, key=SECRET_KEY, algorithm="HS256")


def jdecode(token):
    try:
        return jwt.decode(jwt=token,
                          key=SECRET_KEY,
                          leeway=datetime.timedelta(seconds=86400),
                          algorithms=["HS256"])
    except Exception as e:
        print(e)
        return None


if __name__ == "__main__":
    print(jdecode(jencode({"username": "admin"})))
