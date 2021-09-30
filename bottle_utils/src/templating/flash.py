#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Flash module for capturing errors/info to display back to customers

Flashes are used to notify the customer of an error in a form or other input
This module defines a flash object to use to define an error and associated
display level

"""
from enum import Enum


class Flash:
    """A Class representing a message to show to an app user

    Flashes have a flash level which is like a log level for customer
    facing notifications

    """

    def __init__(self, level, message):
        if not isinstance(level, FlashLvl):
            raise ValueError("level must be a valid FlashLvl")

        self._level = level
        self.msg = message

    @property
    def lvl(self):
        """Level formatted for use in css"""
        return self._level.name.lower()


class FlashLvl(Enum):
    """ Level (think log level) of notification"""

    INFO = 0
    WARN = 1
    ERROR = 2
