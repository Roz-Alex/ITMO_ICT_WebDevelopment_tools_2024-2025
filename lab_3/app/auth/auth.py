import datetime

import jwt
from fastapi import Security, HTTPException, FastAPI
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from starlette import status

from repos.user_repos import find_user


class AuthService:
    """
    Handles user authentication: password hashing, JWT token management, and user validation.
    """

    def __init__(self):
        self.pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")
        self.secret = 'mysecretverylongversion'

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def verify_password(self, pwd, hashed_pwd):
        return self.pwd_context.verify(pwd, hashed_pwd)

    def encode_token(self, user_id):
        """
        Encodes the given user_id into a JWT token.
        :param user_id: <int>
        :return: <str> JWT token
        """
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=8),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }

        return jwt.encode(payload, self.secret, algorithm='HS256')

    def decode_token(self, token):
        """
        Decodes the given token from the JWT token.
        :param token: <str> JWT token
        :return: <str> user email
        """
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            return payload['sub']

        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Expired signature')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail='Invalid token')

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(HTTPBearer())):
        return self.decode_token(auth.credentials)

    def get_current_user(self, auth: HTTPAuthorizationCredentials = Security(HTTPBearer())):
        """
        Returns the current user if authenticated.
        :param auth: Authorization credentials
        :return: user
        """
        credentials_exc = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials'
        )
        email = self.decode_token(auth.credentials)
        if email is None:
            raise credentials_exc
        user = find_user(email)
        if user is None:
            raise credentials_exc
        return user