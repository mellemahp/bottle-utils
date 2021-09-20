#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""/app/auth.py
Description: Defines the basic authentication functionalities of the application
    this could be things like validating a JWT or other fancy stuff or checking for 
    a valid session, etc. 
Project: Python App Template
Author: Hunter Mellema
Date: 1/20/2020
"""
# === Start imports ===#
# standard library imports
import structlog

# third party imports
from bottle import request, redirect, abort, HTTPError

# local imporst
from utils.tokens.session import InvalidSessionException, SESSION_COOKIE_NAME
from utils.tokens.csrf import CSRF_FIELD_NAME
from utils.flash import Flash, FlashLvl

# === End Imports ===#

def session_auth(fxn):
    """Generate a new function that validates the request before allowing access to a route

    """
    def wrapper(*args, **kwargs): 
        if 'session' in kwargs:
            return fxn(*args, **kwargs)

        try: 
            token = request.get_cookie(SESSION_COOKIE_NAME, default=None)
            session = request.app.session_mgr.get_session_from_token(token)

            return fxn(*args, session=session, **kwargs)

        except InvalidSessionException as exc:
            return redirect('/login')

        except Exception as exc:
            log = structlog.get_logger(__name__)
            log.error("Failed authorization")
            log.error(exc) 

            return abort(500, "Internal Service Error")

    return wrapper


def csrf_form(form_class):
    """Generate a form with csrf

    """
    def decorator(fxn):
        def wrapper(*args, **kwargs):
            # If the form is already being passed in then the function is being called by another 
            # route internally and we can just return
            if 'form' in kwargs:
                return fxn(*args, **kwargs)
            
            if request.method == 'POST': 
                form = form_class(
                    request.POST, 
                    meta={
                        'csrf_token_mgr': request.app.csrf_mgr,
                        'session': kwargs.get('session', None)
                    }
                )

                if form.validate():
                    return fxn(*args, form=form, **kwargs)

                elif form.errors:
                    errors = [
                        Flash(FlashLvl.ERROR, error[0]) for 
                        error in [
                            form.errors[field]
                            for field in form.errors.keys()
                        ]
                    ]

                    return fxn(*args, form=form, errors=errors, **kwargs)


            # Form needs to be built for a get route
            elif request.method == 'GET':
                form = form_class(
                    meta={
                        'csrf_token_mgr': request.app.csrf_mgr,
                        'session': kwargs.get('session', None)
                    }
                )
                return fxn(*args, form=form, **kwargs)
            else: 
                raise ValueError("This branch should not be reachable. Something went terribly wrong")

        return wrapper

    return decorator

# TODO: Update to somthing reasonable
DEFAULT_MAX_RATE_PER_SECOND = 20122321321
def rate_limit(*args):
    """ Limits the number of requests to this API for a given API
    """ 
    def _rate_limit(fxn):
        def wrapper(*args, **kwargs): 
            log = structlog.get_logger(__name__)
            try: 
                counter = request.app.rate_limit_mgr.get_or_create_counter()

                if counter.value > max_rate_per_second:
                    log.error(f"Exceeded rate for ip: {request.remote_addr} with counter value: {counter.value}")
                    log.error(f"Rate Exceeded request data: {request}")
                    return HTTPError(status=429, body="Too Many Requests. Wait before retrying")
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