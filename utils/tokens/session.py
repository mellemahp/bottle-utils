#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""/app/utils/sessions.py

Utility functions for managing sessions in the context aware dashboard demo

"""
# === Start imports ===#
import json

from bottle import response

import structlog
from .token_manager import BaseTokenManager
from .csrf import CSRF_FIELD_NAME
# === End Imports ===#

class InvalidSessionException(Exception): 
    pass


SESSION_COOKIE_NAME = "SESSIONID"
SESSION_TOKEN_LENGTH = 36
SESSION_CACHE_PREFIX = "session"
SESSION_EXPIRATION_SEC = 7200
MAX_SESSION_COOKIE_AGE_SEC = 7200

class SessionTokenManager(BaseTokenManager): 

    def __init__(self, csrf_mgr, redis_client):
        super().__init__(
            SESSION_TOKEN_LENGTH, 
            SESSION_EXPIRATION_SEC, 
            SESSION_CACHE_PREFIX, 
            redis_client
        )
        self.csrf_mgr = csrf_mgr
        self.user_to_session_mapper = UserToSessionTokenManager(redis_client)

    
    def create_and_set_session(self, user):
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
            samesite="Strict"
        ) 


    def create_session(self, user): 
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
            csrf_token
        )

        self.set_token_data(session_token, session.__dict__())
        
        return session
    

    def get_session_from_token(self, token):
        if token == None: 
            raise InvalidSessionException("No Session data found")
        
        if self.does_token_exist(token):
            session_data = self.get_token_data(token)
            self.refresh_token(token)

            return Session.from_jsons(token, session_data)

        raise InvalidSessionException("Invalid Session data")

        
    def expire_session(self, session): 
        self.expire_token(session.session_id)
        self.user_to_session_mapper.expire_user_session_entry(session.user_uuid)


USER_TO_SESSION_CACHE_PREFIX = "user_to_sess"

class UserToSessionTokenManager(BaseTokenManager):

    def __init__(self, redis_client):
        super().__init__(
            None,
            SESSION_EXPIRATION_SEC, 
            USER_TO_SESSION_CACHE_PREFIX, 
            redis_client
        )

    def does_user_session_exist(self, user): 
        return self.does_token_exist(user.uuid)

    def get_user_session(self, user):
        return self.get_token_data(user.uuid)
       
    def expire_user_session_entry(self, user): 
        return self.expire_token(user.uuid)

    def create_user_to_session_entry(self, user, session): 
        self.set_token_data(user.uuid, session.session_id)


USER_ID_KEY = "user_uuidd"
USERNAME_KEY = "username"
EMAIL_KEY = "email"
SETTINGS = "settings"

class Session(): 

    #TODO: Session id's should be encrypted when read
    def __init__(self, session_id, user_uuid, username, email, user_settings, csrf_token):
        self.session_id = session_id
        self.user_uuid = user_uuid
        self.username = username
        self.email = email
        self.user_settings = user_settings
        self.csrf_token = csrf_token
        

    @classmethod
    def from_jsons(cls, session_id, json_string):
        return cls.from_dict(session_id, json.loads(json_string))


    @classmethod
    def from_dict(cls, session_id, data):
        return Session(
            session_id,
            data[USER_ID_KEY],
            data[USERNAME_KEY],
            data[EMAIL_KEY],
            data[SETTINGS],
            data[CSRF_FIELD_NAME]
        )


    def __dict__(self): 
        return {
            USER_ID_KEY: self.user_uuid,
            USERNAME_KEY: self.username, 
            EMAIL_KEY: self.email,
            CSRF_FIELD_NAME: self.csrf_token,
            SETTINGS: self.user_settings
        }
