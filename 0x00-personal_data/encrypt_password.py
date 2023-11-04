#!/usr/bin/env python3
"""password encryption"""

import bcrypt


def hash_password(password: str) -> bytes:
    """returns a hashed password, which is a byte string"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """check if a password is valid"""
    if bcrypt.checkpw(bytes(password, 'utf-8'), hashed_password):
        return True
    return False
