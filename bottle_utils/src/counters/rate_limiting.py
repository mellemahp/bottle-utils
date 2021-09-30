#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Counter object for rate limiting routes


"""
import json
from bottle import request
from bottle_utils.src.monitoring.logging import LogMixin
import hashlib

RATE_LIMIT_PREFIX = "rate_limit"
RATE_LIMIT_COUNTER_EXPIRATION_SEC = 1


class RateLimitCounterManager(LogMixin):
    HASHED_FORMAT_STR = "{ip_addr}{url}"

    def __init__(self, redis_client):
        self.redis_client = redis_client

    def get_or_create_counter(self):
        counter_key = self.get_counter_key()
        if self.redis_client.exists(counter_key):
            value = self.redis_client.get(counter_key)
            return RequestCounter(self.redis_client, counter_key, value)
        else:
            return self.create_counter(counter_key)

    def get_counter_key(self):
        hashed_data = hashlib.sha256(
            self.HASHED_FORMAT_STR.format(
                ip_addr=request.remote_addr, url=request.url
            ).encode("utf8")
        ).hexdigest()

        return f"{RATE_LIMIT_PREFIX}:{hashed_data}"

    def create_counter(self, counter_key):
        self.redis_client.set(counter_key, 1, ex=RATE_LIMIT_COUNTER_EXPIRATION_SEC)
        return RequestCounter(self.redis_client, counter_key, 1)


class RequestCounter:
    def __init__(self, redis_client, counter_key, value):
        self.redis_client = redis_client
        self.counter_key = counter_key
        self.value = value

    def increment(self):
        self.redis_client.incr(self.counter_key)
        self.value += 1
