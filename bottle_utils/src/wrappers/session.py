#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Session management wrappers for bottle routes

Allows clean checking of authorization to be added to bottle routes using
a decorator

"""
from bottle_utils.src.tokens.session import SESSION_COOKIE_NAME, InvalidSessionException
from bottle import request, redirect


def session_auth(fxn):
    """Validates the request has a valid session before allowing access to a route"""

    def wrapper(*args, **kwargs):
        if "session" in kwargs:
            return fxn(*args, **kwargs)

        try:
            token = request.get_cookie(SESSION_COOKIE_NAME, default=None)
            # pylint: disable=no-member
            session = request.app.session_mgr.get_session_from_token(token)

            return fxn(*args, session=session, **kwargs)

        except InvalidSessionException:
            return redirect("/login")

    return wrapper
