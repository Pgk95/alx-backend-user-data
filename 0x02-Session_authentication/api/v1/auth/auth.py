#!/usr/bin/env python3
"""Auth module"""

from flask import request
from typing import List, TypeVar
import os

class Auth:
    """Auth class"""

    def require_auth(self, path: str, excuded_paths: List[str]) -> bool:
        """Require auth"""
        if path is None or excuded_paths is None or excuded_paths == []:
            return True
        if path[-1] != '/':
            path += '/'
        if path in excuded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """Authorization header"""
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None
        else:
            return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """Current user"""
        if request is None:
            return None
    
    def session_cookie(self, request=None):
        """Session cookie"""
        if request is None:
            return None
        if os.getenv('SESSION_NAME') not in request.cookies:
            return None
        return request.cookies.get(os.getenv('SESSION_NAME'))
