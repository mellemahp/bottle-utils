#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CSRF manager for use with WTForms form

Defines manager classes that handles the creation, deletion, 
and validation of CSRF tokens for WTForms forms

Currently supported session stores: 
- Redis

"""
from wtforms.csrf.core import CSRF
from bottle_utils.src.tokens.token_manager import BaseTokenManager
from bottle_utils.src.tokens.csrf import CSRFInvalidException


class RedisCacheCSRF(CSRF):
    """
    Generate a CSRF token for form using a token provider based on storing CSRF
    tokens in a redis key-value store
    """

    def setup_form(self, form):
        # Check that the token manager exists and is a TokenManager
        if not isinstance(form.meta.csrf_token_mgr, BaseTokenManager):
            raise ValueError(
                "CSFR Token manager must be an instance of BaseTokenManager"
            )

        # pylint: disable=attribute-defined-outside-init
        self.csrf_token_mgr = form.meta.csrf_token_mgr
        # pylint: disable=attribute-defined-outside-init
        self.session = form.meta.session

        return super().setup_form(form)

    def generate_csrf_token(self, csrf_token_field):
        if self.session is None:
            return self.csrf_token_mgr.create_sessionless_csrf_token()

        return self.session.csrf_token

    def validate_csrf_token(self, form, field):
        token = field.data
        try:
            if self.session is None:
                self.csrf_token_mgr.validate_sessionless_csrf(token)
            else:
                self.csrf_token_mgr.validate_csrf_session_token(token, self.session)
        except CSRFInvalidException as exc:
            raise ValueError from exc
