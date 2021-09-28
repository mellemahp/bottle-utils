"""
Counter object for rate limiting 
"""
# === Start imports ===#
import json

from bottle import request

from utils.logging import LogMixin

import hashlib
# === End Imports ===#

RATE_LIMIT_PREFIX = "rate_limit"
RATE_LIMIT_COUNTER_EXPIRATION_SEC = 1

class RateLimitCounterManager(LogMixin):
    
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
        ip_addr = request.remote_addr
        url = request.url
        hashed_data = hashlib.md5(f"{ip_addr}{url}".encode('utf8')).hexdigest()

        return f"{RATE_LIMIT_PREFIX}:{hashed_data}"

    def create_counter(self, counter_key): 
        self.redis_client.set(
            counter_key, 1, 
            ex=RATE_LIMIT_COUNTER_EXPIRATION_SEC
        )
        return RequestCounter(self.redis_client, counter_key, 1)


class RequestCounter(): 
    
    def __init__(self, redis_client, counter_key, value): 
        self.redis_client = redis_client
        self.counter_key = counter_key
        self.value = value

    def increment(self):
        self.redis_client.incr(self.counter_key)
        self.value += 1




