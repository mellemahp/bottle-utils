#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Common Validation models for Bottle applications using WTForms

Defines a set of common validation models that can be re-used accross multiple
WTForm forms

Example Usage:
```
from wtforms import Form

class LoginForm(Form):
    username = USERNAME
    password = PASSWORD
    
```

"""
from wtforms import HiddenField, PasswordField, StringField, validators

# Username that cannot contain any special characters
USERNAME_REGEX = r"^[a-zA-Z0-9]*$"
USERNAME = StringField(
    "Username",
    [
        validators.Regexp(USERNAME_REGEX, message="Invalid Username."),
        validators.Length(
            min=4, max=25, message="Username must be between 4 to 25 characters"
        ),
        validators.InputRequired(),
    ],
)

PASSWORD = PasswordField(
    "Password",
    [
        validators.Length(
            min=6, max=35, message="Password must be between 6 to 35 characters"
        ),
        validators.InputRequired(),
    ],
)

PASSWORD_REGEX = (
    r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{6,}$"  # nosec
)
PASSWORD_CONFIRMATION = PasswordField(
    "Confirm Password",
    [
        validators.Regexp(
            PASSWORD_REGEX,
            message="Password must have at least one letter, number, and special character",
        ),
        validators.InputRequired(),
        validators.EqualTo("password", message="Passwords must match"),
    ],
)


EMAIL = StringField(
    "Email",
    [
        validators.Email(message="Invalid Email Format"),
        validators.Length(min=6, max=35, message="Invalid Email length"),
        validators.InputRequired(),
    ],
)

EMAIL_VERIFICATION_TOKEN = HiddenField(
    "VerificationToken",
    [
        validators.Length(min=20, max=20, message="Bad Validation Token"),
        validators.InputRequired(),
    ],
)
