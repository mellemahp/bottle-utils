#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Classes and functions for managing CSRF tokens for Bottle apps

Token manager class and associated settings and exceptions for 
managing CSRF tokens using Redis as the Backend data store

"""
from bottle_utils.src.tokens.token_manager import BaseTokenManager

CSRF_FIELD_NAME = "CSRFToken"
CSRF_TOKEN_LENGTH = 36
TEMP_CSRF_KEY_PREFIX = "temp-csrf"
CSRF_SESSIONLESS_EXPIRATION_SEC = 600


class CSRFInvalidException(Exception):
    """Invalid or Non-existant CSRF token"""


class CSRFTokenManager(BaseTokenManager):
    """Manager for CSRF tokens stored in a redis-based session store"""

    def __init__(self, redis_client):
        super().__init__(
            CSRF_TOKEN_LENGTH,
            CSRF_SESSIONLESS_EXPIRATION_SEC,
            TEMP_CSRF_KEY_PREFIX,
            redis_client,
        )

    def create_sessionless_csrf_token(self):
        """Creates a session token in the session store

        Returns:
            String: session token
        """
        token = self.generate_token()
        self.set_token_data(token, "")

        return token

    def expire_sessionless_csrf_token(self, token):
        """Expires a session in the session store

        Args:
            token (str): session token to expire

        """
        try:
            self.validate_sessionless_csrf(token)
            self.expire_token(token)
        except CSRFInvalidException:
            pass

    def validate_sessionless_csrf(self, token):
        """Checks that the csrf token is in the session store

        Args:
            token (str): token to check against session store

        Raises:
            CSRFInvalidException: Bad or no csrf token

        """
        if token is None:
            raise CSRFInvalidException("No CSRF Token")

        if not self.does_token_exist(token):
            raise CSRFInvalidException("Invalid CSRF Token")

    def validate_csrf_session_token(self, token, session):
        """Checks that the csrf token matches that on a session

        Args:
            token (str): token to check against user session
            session (Session): user session

        Raises:
            CSRFInvalidException: Bad or no csrf token

        """
        if token is None:
            raise CSRFInvalidException("No CSRF Token")

        if token != session.csrf_token:
            raise CSRFInvalidException("Invalid CSRF Token")
