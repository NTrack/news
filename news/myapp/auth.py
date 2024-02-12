from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

from .utils import *


class TokenAuthenticate(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get('Authorization')
        if token is not None:
            token = token.split(' ')[-1]
            if verify_jwt(token):
                user = get_user_by_jwt(token)
                return user, token
        raise exceptions.AuthenticationFailed('认证失败')

    def authenticate_header(self, request):
        pass
