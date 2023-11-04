#!/usr/bin/env python3
"""log message obfuscated"""


import re


def filter_datum(fields: list[str], redaction: str, message: str,
                 separator: str) -> str:
    """returns the log message obfuscated"""
    for i in fields:
        message = re.sub(rf'{i}=.*?{separator}',
                         f'{i}={redaction}{separator}', message)
        return message
