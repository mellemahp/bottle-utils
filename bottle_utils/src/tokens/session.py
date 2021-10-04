#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Classes and functions for managing Session tokens for Bottle apps

Token manager class and associated settings and exceptions for 
managing Session tokens using Redis as the Backend data store

"""
import json
from bottle import response
from bottle_utils.src.tokens.token_manager import BaseTokenManager
from bottle_utils.src.tokens.csrf import CSRF_FIELD_NAME


class InvalidSessionException(Exception):
    """Session does not exist or is invalid"""


SESSION_COOKIE_NAME = "SESSIONID"
SESSION_TOKEN_LENGTH = 36
SESSION_CACHE_PREFIX = "session"
SESSION_EXPIRATION_SEC = 7200
MAX_SESSION_COOKIE_AGE_SEC = 7200


class SessionTokenManager(BaseTokenManager):
    """Manager for Session data and tokens stored in a redis-based session store"""

    def __init__(self, csrf_mgr, redis_client):
        super().__init__(
            SESSION_TOKEN_LENGTH,
            SESSION_EXPIRATION_SEC,
            SESSION_CACHE_PREFIX,
            redis_client,
        )
        self.csrf_mgr = csrf_mgr
        self.user_to_session_mapper = UserToSessionTokenManager(redis_client)

    def create_and_set_session(self, user):
        """Create a session in the session store for a given user

        Args:
            user (User): user to set session for

        Notes:
            - Sets the session token as a cookie in the bottle route response

        """
        # Delete any existing sessions if they exist
        if self.user_to_session_mapper.does_user_session_exist(user):
            session = self.user_to_session_mapper.get_user_session(user)
            self.expire_session(session)
            self.user_to_session_mapper.expire_user_session_entry(user)

        session = self.create_session(user)
        self.user_to_session_mapper.create_user_to_session_entry(user, session)

        # TODO: Add Secure once HTTPS supported
        response.set_cookie(
            SESSION_COOKIE_NAME,
            session.session_id,
            max_age=MAX_SESSION_COOKIE_AGE_SEC,
            httponly=True,
            samesite="Strict",
        )

    def create_session(self, user):
        """Creates a session for a user

        Args:
            user (User): user to create session for

        Returns:
            Session

        """
        csrf_token = self.csrf_mgr.generate_token()
        session_token = self.generate_token()

        # TODO: Add user settings?
        dummy_settings = {"test": "A"}

        session = Session(
            session_token,
            user.uuid,
            user.username,
            user.email,
            dummy_settings,
            csrf_token,
        )

        self.set_token_data(session_token, session.to_dict())

        return session

    def get_session_from_token(self, token):
        """Gets a session object from a session token

        Args:
            token (str): session token

        Returns:
            Session

        Raises:
            InvalidSessionException: Session is not valid

        """
        if token is None:
            raise InvalidSessionException("No Session data found")

        if not self.does_token_exist(token):
            raise InvalidSessionException("Invalid Session data")

        session_data = self.get_token_data(token)
        self.refresh_token(token)

        return Session.from_jsons(token, session_data)

    def expire_session(self, session):
        """Expires a session

        Args:
            session (Session): session to expire

        """
        self.expire_token(session.session_id)
        self.user_to_session_mapper.expire_user_session_entry(session.user_uuid)


USER_TO_SESSION_CACHE_PREFIX = "user_to_sess"


class UserToSessionTokenManager(BaseTokenManager):
    """Manager for token that maps session to user name"""

    def __init__(self, redis_client):
        super().__init__(
            None, SESSION_EXPIRATION_SEC, USER_TO_SESSION_CACHE_PREFIX, redis_client
        )

    def does_user_session_exist(self, user):
        """Checks for user having a session"""
        return self.does_token_exist(user.uuid)

    def get_user_session(self, user):
        """Gets session data for user"""
        return self.get_token_data(user.uuid)

    def expire_user_session_entry(self, user):
        """Expires user/session entry"""
        return self.expire_token(user.uuid)

    def create_user_to_session_entry(self, user, session):
        """Creates a new user/session mapping entry"""
        self.set_token_data(user.uuid, session.session_id)


USER_ID_KEY = "user_uuidd"
USERNAME_KEY = "username"
EMAIL_KEY = "email"
SETTINGS = "settings"


class Session:
    """Container Class for sessions"""

    # TODO: Session id's should be encrypted when read
    def __init__(
        self, session_id, user_uuid, username, email, user_settings, csrf_token
    ):
        self.session_id = session_id
        self.user_uuid = user_uuid
        self.username = username
        self.email = email
        self.user_settings = user_settings
        self.csrf_token = csrf_token

    @classmethod
    def from_jsons(cls, session_id, json_string):
        """Get a session from a json string

        Args:
            session_id (str): session id
            json_string (str): json string of session data

        """
        return cls.from_dict(session_id, json.loads(json_string))

    @classmethod
    def from_dict(cls, session_id, data):
        """Gets a session from a dictionary object"""
        return Session(
            session_id,
            data[USER_ID_KEY],
            data[USERNAME_KEY],
            data[EMAIL_KEY],
            data[SETTINGS],
            data[CSRF_FIELD_NAME],
        )

    def to_dict(self):
        return {
            USER_ID_KEY: self.user_uuid,
            USERNAME_KEY: self.username,
            EMAIL_KEY: self.email,
            CSRF_FIELD_NAME: self.csrf_token,
            SETTINGS: self.user_settings,
        }
