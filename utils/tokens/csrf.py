#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""/app/utils/sessions.py

Utility functions for managing sessions in the context aware dashboard demo

"""
# === Start imports ===#
from .token_manager import BaseTokenManager

# === End Imports ===#

CSRF_FIELD_NAME = "CSRFToken"
CSRF_TOKEN_LENGTH = 36
TEMP_CSRF_KEY_PREFIX = "temp-csrf"
CSRF_SESSIONLESS_EXPIRATION_SEC = 600

class CSRFInvalidException(Exception): 
    pass


class CSRFTokenManager(BaseTokenManager): 


    def __init__(self, redis_client):
        super().__init__(
            CSRF_TOKEN_LENGTH, 
            CSRF_SESSIONLESS_EXPIRATION_SEC, 
            TEMP_CSRF_KEY_PREFIX, 
            redis_client
        )


    def is_valid_sessionless_csrf(self, token): 
        return self.does_token_exist(token)


    def expire_sessionless_csrf_token(self, token):
        if self.is_valid_sessionless_csrf(token): 
            self.expire_token(token)


    def validate_csrf_session_token(self, token, session): 
        if token == None:
            raise CSRFInvalidException("No CSRF Token")

        elif token != session.csrf_token: 
            raise CSRFInvalidException("Invalid CSRF Token")
        
        else: 
            return True


    def create_sessionless_csrf_token(self): 
        token = self.generate_token()
        self.set_token_data(token, "")

        return token

