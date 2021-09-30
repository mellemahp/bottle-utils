#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Base class for managing Tokens in a Bottle app using Redis

Base Token manager class and associated settings and exceptions for 
managing tokens using Redis as the Backend data store

"""
import json
import random
import string
from uuid import UUID
from bottle_utils.src.monitoring.logging import LogMixin


class TokenException(Exception):
    """Generic exception for CRUD operations on tokens"""


class TokenReadException(TokenException):
    """Thrown when token cannot be read from db"""


class TokenWriteException(TokenException):
    """Thrown when token cannot be written to db"""


class TokenExpirationException(TokenException):
    """Thrown when token expiration cannot be set"""


class TokenRefreshException(TokenException):
    """Exception thrown when token expiration refresh fails"""


class BaseTokenManager(LogMixin):
    """Base class for managers of tokens stored in redis"""

    def __init__(
        self, token_length, token_expiration_sec, token_cache_prefix, redis_client
    ):
        self.token_length = token_length
        self.token_expiration_sec = token_expiration_sec
        self.token_cache_prefix = token_cache_prefix
        self.redis_client = redis_client

    def does_token_exist(self, token):
        """Checks for token in key-value store

        Arguments:
            token (str): key value to check for in key-value store

        Raises:
            TokenReadException: unable to reach key-value store
        """
        try:
            return self.redis_client.exists(f"{self.token_cache_prefix}:{token}")

        except Exception as exc:
            self.log.error(exc)
            raise TokenReadException("Failed to access Token cache")

    def expire_token(self, token):
        """Removes a token from the key-value store

        Args:
            token (str): token to expire

        Raises:
            TokenExpirationException: raised on failure to delete

        """
        try:
            self.redis_client.delete(f"{self.token_cache_prefix}:{token}")

        except Exception as exc:
            self.log.error(exc)
            raise TokenExpirationException("Could Not Expire Token")

    def refresh_token(self, token):
        """Resets the expiration time of a token

        Args:
            token (str): token to reset expiration time for

        Raises:
            TokenRefreshException: raised on failure to edit

        """
        try:
            self.redis_client.expire(token, self.token_expiration_sec)

        except Exception as exc:
            self.log.error(exc)
            raise TokenRefreshException("Could not refresh Token")

    def get_token_data(self, token):
        """Gets data attached to a token `key` in the key-value store

        Args:
            token (str): key to get value for in key-value store

        Raises:
            TokenReadException: error reading key-value store

        """
        try:
            return self.redis_client.get(f"{self.token_cache_prefix}:{token}")

        except Exception as exc:
            self.log.error(exc)
            raise TokenReadException("Failed to read Token Data")

    def set_token_data(self, token, data):
        """Attaches data to the key (token) value in the key-value store

        Args:
            token (str):
            data (<? encodable to json>): Some data that can be converted
                to a json-formatted string

        Raises:
            TokenWriteException: error writing to key-value store

        Notes:
            - Sets a default expiration time on this data

        """
        try:
            self.redis_client.set(
                f"{self.token_cache_prefix}:{token}",
                json.dumps(data, cls=UUIDEncoder),
                ex=self.token_expiration_sec,
            )

        except Exception as exc:
            self.log.error(exc)
            raise TokenWriteException("Could not write token data to cache")

    def generate_token(self):
        """Generates a random token of some length

        Returns:
            String

        Notes:
            - Requires a default token length to be set
            - Uses the system random generator for maximal randomness

        """
        return "".join(
            random.SystemRandom().choice(
                string.ascii_lowercase + string.ascii_uppercase + string.digits
            )
            for _ in range(self.token_length)
        )


class UUIDEncoder(json.JSONEncoder):
    """UUID encoder to allow the writing of UUID's to json format"""

    def default(self, o):
        if isinstance(o, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return o.hex
        return json.JSONEncoder.default(self, o)
