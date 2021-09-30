#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CSRF management wrappers for bottle routes

Allows users to add csrf-enabled WTForms form to a route.

"""
from bottle_utils.src.templating.flash import Flash, FlashLvl
from bottle import request


def csrf_form(form_class):
    """Generate form with csrf for a route to return to a user"""

    def decorator(fxn):
        def wrapper(*args, **kwargs):
            # If the form is already being passed in then the function is being
            # called by another route internally and we can just return
            if "form" in kwargs:
                return fxn(*args, **kwargs)

            if request.method == "POST":
                form = form_class(
                    request.POST,
                    meta={
                        # pylint: disable=no-member
                        "csrf_token_mgr": request.app.csrf_mgr,
                        "session": kwargs.get("session", None),
                    },
                )

                if form.validate():
                    return fxn(*args, form=form, **kwargs)

                if form.errors:
                    errors = [
                        Flash(FlashLvl.ERROR, error[0])
                        for error in [
                            form.errors[field] for field in form.errors.keys()
                        ]
                    ]

                    return fxn(*args, form=form, errors=errors, **kwargs)

                raise ValueError(
                    "Internal Service Error. Something went terribly wrong"
                )

            # Form needs to be built for a get route
            if request.method == "GET":
                form = form_class(
                    meta={
                        # pylint: disable=no-member
                        "csrf_token_mgr": request.app.csrf_mgr,
                        "session": kwargs.get("session", None),
                    }
                )
                return fxn(*args, form=form, **kwargs)

            raise ValueError("Internal Service Error. Something went terribly wrong")

        return wrapper

    return decorator
