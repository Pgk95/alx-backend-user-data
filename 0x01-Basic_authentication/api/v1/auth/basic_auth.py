#!/usr/bin/env python3
"""basic auth class"""
from api.v1.auth.auth import Auth
from base64 import b64decode, decode
from typing import TypeVar
import base64


class BasicAuth(Auth):
    """BasicAuth class"""

    def extract_base64_authorization_header(self, auth_header: str) -> str:
        """returns the Base64 part of the authorization header"""
        if auth_header is None or not isinstance(auth_header, str):
            return None
        if 'Basic ' not in auth_header:
            return None
        return auth_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_auth_header: str) -> str:
        """returns the decoded value of a
            base64 string
        """
        if base64_auth_header is None or not isinstance(base64_auth_header,
                                                        str):
            return None
        try:
            return base64.b64decode(base64_auth_header).decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str) -> (
                                         str, str):
        """returns the user email and
           password from the Base64 decoded value
        """
        if decoded_base64_authorization_header is None or not isinstance(
                decoded_base64_authorization_header, str) or ':' not in \
                decoded_base64_authorization_header:
            return None, None
        return tuple(decoded_base64_authorization_header.split(':', 1))

    def user_object_from_credentials(self, user_email:
                                     str, user_pwd: str) -> TypeVar('User'):
        """returns the user instance based
           on his email and password
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            from models.user import User
            users = User.search({'email': user_email})
        except Exception:
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """applying all previous methods to return"""
        auth_header = self.authorization_header(request)
        extract_base64 = self.extract_base64_authorization_header(auth_header)
        decode_base64 = self.decode_base64_authorization_header(extract_base64)
        extract_user_credentials = self.extract_user_credentials(decode_base64)
        user_object_credentials = self.user_object_from_credentials(
            user_email=extract_user_credentials[0],
            user_pwd=extract_user_credentials[1]
        )
        return user_object_credentials
