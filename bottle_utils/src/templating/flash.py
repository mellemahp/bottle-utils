#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Flash module for capturing errors/info to display back to customers

Flashes are used to notify the customer of an error in a form or other input
This module defines a flash object to use to define an error and associated
display level

"""
from enum import Enum


class FlashLvl(Enum):
    INFO = 0
    WARN = 1
    ERROR = 2


class Flash:
    def __init__(self, level, message):
        if not isinstance(level, FlashLvl):
            raise ValueError("level must be a valid FlashLvl")

        self._level = level
        self.msg = message

    @property
    def lvl(self):
        return self._level.name.lower()
