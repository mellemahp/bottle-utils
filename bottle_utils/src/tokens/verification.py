#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Module for managing email validation Tokens in a Bottle app using Redis

Token manager class and associated settings and exceptions for 
managing Email validation tokens using Redis as the Backend data store

"""
from bottle_utils.src.tokens.token_manager import BaseTokenManager
import json


VERIFICATION_TOKEN_LENGTH = 20
VERIFICATION_KEY_PREFIX = "email-verification"
VERIFICATION_TOKEN_EXPIRATION_SEC = 86400  # 1 day in seconds


class VerificationTokenInvalidException(Exception):
    """Invalid Email verification token"""


class VerificationTokenManager(BaseTokenManager):
    """Manager for email verification tokens stored redis key-value store"""

    def __init__(self, redis_client):
        super().__init__(
            VERIFICATION_TOKEN_LENGTH,
            VERIFICATION_TOKEN_EXPIRATION_SEC,
            VERIFICATION_KEY_PREFIX,
            redis_client,
        )

    def is_valid_verification_token(self, token):
        """Checks if token is in key-value store"""
        return self.does_token_exist(token)

    def expire_verification_token(self, token):
        """Expires email verification token in key-value store"""
        self.expire_token(token)

    def get_verification_token_user_data(self, token):
        """Gets user associated with the email verification token

        Args:
            token (str): email verification token

        Raises:
            VerificationTokenInvalidException: bad email verification token

        Returns:
            Dict: user data

        """
        if token is None:
            raise VerificationTokenInvalidException("No Email Validation Token")

        if not self.is_valid_verification_token(token):
            raise VerificationTokenInvalidException("Invalid Email Validation Token")

        return json.loads(self.get_token_data(token))

    def create_email_verification_token(self, user):
        """Generates a new email verification token for a user
        Note: Sets token in key-value store

        Args:
            user (User): user to generate token for

        Returns:
            String: verification token string

        """
        token = self.generate_token()
        data = {"user_id": user.uuid}
        self.set_token_data(token, data)

        return token
