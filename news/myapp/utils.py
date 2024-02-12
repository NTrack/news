import time
from typing import Any

import jwt

from .models import Users

# TODO: 环境变量
JWT_TOKEN_EXPIRE_TIME = 60 * 60 * 24 * 7
JWT_SECRET = 'secret'


def create_jwt(openid) -> str:
    [user, _] = Users.objects.get_or_create(openid=openid)
    payload = {
        'data': {
            'openid': openid,
            'user_id': user.user_id
        },
        'exp': int(time.time()) + JWT_TOKEN_EXPIRE_TIME
    }
    return jwt.encode(payload, JWT_SECRET, algorithm='HS256')


def verify_jwt(token) -> bool:
    try:
        jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        return True
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False
    except jwt.PyJWTError:
        return False


def get_user_by_jwt(token) -> Any | None:
    match verify_jwt(token):
        case True:
            openid = jwt.decode(token, JWT_SECRET, algorithms=['HS256']).get('data').get('openid')
            [user, _] = Users.objects.get_or_create(openid=openid)
            return user
        case False:
            return None
