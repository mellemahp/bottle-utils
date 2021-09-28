#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Redis connectors

Connectors for both real redis backends as well as local mock redis backends

"""
import os
import structlog

from redis import StrictRedis
from redislite import Redis

log = structlog.get_logger(__name__)

LOCAL_REDIS_FILENAME = "redis.db"


def connect_to_redis():
    """
    Establishes a connection to the redis session store

    Returns:
        redis.StrictRedis

    Notes:
        Edits application in place
        Needs the following Environment variables:
            SESSION_STORE_HOST (name of contiainer with redis)
            SESSION_STORE_PORT (open port for redis connection)
            SESSION_PASS (password for redis database)
    """
    log.info("Connecting to redis...")
    redis_conn = StrictRedis(
        host=os.environ.get("SESSION_STORE_HOST"),
        port=int(os.environ.get("SESSION_STORE_PORT")),
        password=os.environ.get("SESSION_PASS"),
    )
    log.info("Connected to redis!")
    return redis_conn


def connect_to_redislite_local():
    """
    Establishes a connection to a local python implementation of redis (redislite) for local testing

    Returns:
        redislite.Redis

    Notes:
        Creates a file locally to act as a local redis database

    """
    log.info("Connecting to redislite (local)...")
    redis_conn = Redis(LOCAL_REDIS_FILENAME)
    log.info("Connected to redis!")

    return redis_conn