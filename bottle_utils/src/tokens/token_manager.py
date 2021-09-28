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
from abc import ABCMeta, abstractproperty


class TokenException(Exception):
    pass


class TokenReadException(TokenException):
    pass


class TokenWriteException(TokenException):
    pass


class TokenExpirationException(TokenException):
    pass


class TokenRefreshException(TokenException):
    pass


class BaseTokenManager(LogMixin):
    def __init__(
        self, token_length, token_expiration_sec, token_cache_prefix, redis_client
    ):
        self.token_length = token_length
        self.token_expiration_sec = token_expiration_sec
        self.token_cache_prefix = token_cache_prefix
        self.redis_client = redis_client

    def does_token_exist(self, token):
        try:
            return self.redis_client.exists(f"{self.token_cache_prefix}:{token}")

        except Exception as exc:
            self.log.error(exc)
            raise TokenReadException("Failed to access Token cache")

    def expire_token(self, token):
        try:
            self.redis_client.delete(f"{self.token_cache_prefix}:{token}")

        except Exception as exc:
            self.log.error(exc)
            raise TokenExpirationException("Could Not Expire Token")

    def refresh_token(self, token):
        try:
            self.redis_client.expire(token, self.token_expiration_sec)

        except Exception as exc:
            self.log.error(exc)
            raise TokenRefreshException("Could not refresh Token")

    def get_token_data(self, token):
        try:
            return self.redis_client.get(f"{self.token_cache_prefix}:{token}")

        except Exception as exc:
            self.log.error(exc)
            raise TokenReadException("Failed to read Token Data")

    def set_token_data(self, token, data):
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
        return "".join(
            random.SystemRandom().choice(
                string.ascii_lowercase + string.ascii_uppercase + string.digits
            )
            for _ in range(self.token_length)
        )


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex
        return json.JSONEncoder.default(self, obj)