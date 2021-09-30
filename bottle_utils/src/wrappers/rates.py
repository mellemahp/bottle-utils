#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""


"""
# pylint: skip-file
# TODO: Implement and remove pylint suppression
from bottle import request, redirect, abort, HTTPError
from bottle_utils.src.tokens.session import InvalidSessionException, SESSION_COOKIE_NAME
from bottle_utils.src.tokens.csrf import CSRF_FIELD_NAME
from bottle_utils.src.templating.flash import Flash, FlashLvl


# TODO: Update to somthing reasonable
DEFAULT_MAX_RATE_PER_SECOND = 20122321321


def rate_limit(*args):
    """Limits the number of requests to this API for a given API"""

    def _rate_limit(fxn):
        def wrapper(*args, **kwargs):
            log = structlog.get_logger(__name__)
            try:
                counter = request.app.rate_limit_mgr.get_or_create_counter()

                if counter.value > max_rate_per_second:
                    log.error(
                        f"Exceeded rate for ip: {request.remote_addr} with counter value: {counter.value}"
                    )
                    log.error(f"Rate Exceeded request data: {request}")
                    return HTTPError(
                        status=429, body="Too Many Requests. Wait before retrying"
                    )
                else:
                    counter.increment()
                    return fxn(*args, **kwargs)

            except Exception as exc:
                log.error("Failed Rate Limit Check")
                log.error(exc)

                # TODO: Need to update this to have metrics emitted

                return abort(500, "Internal Service Error")

        return wrapper

    if len(args) == 1 and callable(args[0]):
        # if no arguments present use the defaults
        max_rate_per_second = DEFAULT_MAX_RATE_PER_SECOND
        return _rate_limit(args[0])
    else:
        max_rate_per_second = args[0]
        return _rate_limit
