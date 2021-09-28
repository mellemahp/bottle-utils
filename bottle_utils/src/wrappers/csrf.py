#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""
from bottle_utils.src.templating.flash import Flash, FlashLvl
from bottle import request


def csrf_form(form_class):
    """Generate a form with csrf"""

    def decorator(fxn):
        def wrapper(*args, **kwargs):
            # If the form is already being passed in then the function is being called by another
            # route internally and we can just return
            if "form" in kwargs:
                return fxn(*args, **kwargs)

            if request.method == "POST":
                form = form_class(
                    request.POST,
                    meta={
                        "csrf_token_mgr": request.app.csrf_mgr,
                        "session": kwargs.get("session", None),
                    },
                )

                if form.validate():
                    return fxn(*args, form=form, **kwargs)

                elif form.errors:
                    errors = [
                        Flash(FlashLvl.ERROR, error[0])
                        for error in [
                            form.errors[field] for field in form.errors.keys()
                        ]
                    ]

                    return fxn(*args, form=form, errors=errors, **kwargs)

            # Form needs to be built for a get route
            elif request.method == "GET":
                form = form_class(
                    meta={
                        "csrf_token_mgr": request.app.csrf_mgr,
                        "session": kwargs.get("session", None),
                    }
                )
                return fxn(*args, form=form, **kwargs)
            else:
                raise ValueError(
                    "This branch should not be reachable. Something went terribly wrong"
                )

        return wrapper

    return decorator
