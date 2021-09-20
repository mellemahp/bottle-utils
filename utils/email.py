#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""/app/utils/email.py


"""
# === Start imports ===#
import json

from utils.logging import LogMixin

# === End Imports ===#

class EmailClient(LogMixin): 

    def __init__(self, config):
        pass

    def send_verification_email(self, verification_token, email): 
        # TODO: REMOVE THIS LATER. JUST HELPS TEST VERIFICATION FLOW
        self.log.warn("Sending verification email", token=verification_token, email=email)
    
    def send_password_update_email(self, email):
        self.log.warn("Sending password verification email", email=email)
