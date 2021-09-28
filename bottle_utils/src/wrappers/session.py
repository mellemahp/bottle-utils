#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""


"""
from bottle_utils.src.tokens.session import SESSION_COOKIE_NAME, InvalidSessionException
from bottle import request, redirect
import structlog


def session_auth(fxn):
    """Generate a new function that validates the request before allowing access to a route"""

    def wrapper(*args, **kwargs):
        if "session" in kwargs:
            return fxn(*args, **kwargs)

        try:
            token = request.get_cookie(SESSION_COOKIE_NAME, default=None)
            session = request.app.session_mgr.get_session_from_token(token)

            return fxn(*args, session=session, **kwargs)

        except InvalidSessionException as exc:
            return redirect("/login")

        except Exception as exc:
            log = structlog.get_logger(__name__)
            log.error("Failed authorization")
            log.error(exc)

            return abort(500, "Internal Service Error")

    return wrapper
