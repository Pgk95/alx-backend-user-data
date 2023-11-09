#!/usr/bin/env python3
"""basic auth class"""
from api.v1.auth.auth import Auth
from base64 import b64decode, decode
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
