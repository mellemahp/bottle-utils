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
    pass


class VerificationTokenManager(BaseTokenManager):
    def __init__(self, redis_client):
        super().__init__(
            VERIFICATION_TOKEN_LENGTH,
            VERIFICATION_TOKEN_EXPIRATION_SEC,
            VERIFICATION_KEY_PREFIX,
            redis_client,
        )

    def is_valid_verification_token(self, token):
        return self.does_token_exist(token)

    def expire_verification_token(self, token):
        self.expire_token(token)

    def get_verification_token_user_data(self, token):
        if token is None:
            raise VerificationTokenInvalidException("No Email Validation Token")

        if not self.is_valid_verification_token(token):
            raise VerificationTokenInvalidException("Invalid Email Validation Token")

        return json.loads(self.get_token_data(token))

    def create_email_verification_token(self, user):
        token = self.generate_token()
        data = {"user_id": user.uuid}
        self.set_token_data(token, data)

        return token
