#!/usr/bin/env python3
"""log message obfuscated"""


import re
import os
import logging
import mysql.connector
from typing import List

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Constructor"""
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """filters values in incoming log records using filter_datum"""
        return filter_datum(
            self.fields,
            self.REDACTION,
            super().format(record),
            self.SEPARATOR)


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """returns the log message obfuscated"""
    for i in fields:
        message = re.sub(fr'{i}=.+?{separator}',
                         f'{i}={redaction}{separator}', message)
    return message


def get_logger() -> logging.Logger:
    """returns a logging.logger object"""
    logger = logging.getLogger("user_data")
    handler = logging.StreamHandler()
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(handler)
    return logger


def get_db() -> connection.MySQLConnection:
    """Returns a connector to the database
       (mysql.connector.connection.MySQLConnection) object
    """
        host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
        database = os.getenv('PERSONAL_DATA_DB_NAME'),
        username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
        password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')

        connection = connection.MySQLConnection(
            user=username,
            password=password,
            host=host,
            database=database
        )

        return connection
