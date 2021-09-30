#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""


"""
# pylint: skip-file
# TODO: Implement and remove pylint suppression
import json
from bottle_utils.src.monitoring.logging import LogMixin


class EmailClient(LogMixin):
    def __init__(self, config):
        # TODO: Implement
        pass

    def send_verification_email(self, verification_token, email):
        # TODO: REMOVE THIS LATER. JUST HELPS TEST VERIFICATION FLOW
        self.log.warn(
            "Sending verification email", token=verification_token, email=email
        )

    def send_password_update_email(self, email):
        self.log.warn("Sending password verification email", email=email)
