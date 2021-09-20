#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""/app/utils/db_connectors.py

Functions for connecting to various databases such as Redis and Postgres

"""
# === Start imports ===#
# standard library 
import os
import time
import structlog

from peewee import OperationalError
from redis import StrictRedis
from playhouse.db_url import connect
from peewee import SqliteDatabase

from redislite import Redis

# === End Imports ===#
log = structlog.get_logger(__name__)

LOCAL_REDIS_FILENAME = 'redis.db'
LOCAL_SQLITE_FILENAME = 'test.db'
TEST_TIMEOUT = 100

def connect_to_db(): 
    """
    Established a connection to a Postgresql database
    Returns: 
        peewee.PostgresqlDatabase
    Raises: 
        TimeoutError: couldnt connect to database after ${DB_TIMEOUT} seconds
    Note: 
        Requires a number of environment variables to be set
        [DB_TIMEOUT, DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME]
    """
    log.debug("CONNECTING TO DATABASE")
    wait_time = 0
    timeout = int(os.environ.get("DB_TIMEOUT", 100))
    while wait_time < timeout:
        try:
            db = connect("postgresql://{}:{}@{}:{}/{}".format(
                   os.environ.get("DB_USER"), 
                   os.environ.get("DB_PASS"), 
                   os.environ.get('DB_HOST'), 
                   os.environ.get("DB_PORT"), 
                   os.environ.get("DB_NAME"))
            )
            break

        except OperationalError: 
            log.info("Waiting for database")
            time.sleep(5)
            wait_time += 5
    
    if wait_time > timeout: 
        log.error("Failed to connect to database")
        raise TimeoutError("Database connection attempts timed out")

    log.info("CONNECTED TO DATABASE")


    return db


def connect_to_sqlite_local_db(): 
    """
    Established a connection to a local SQLite database for testing

    Returns: 
        peewee.SqliteDatabase

    Raises: 
        TimeoutError: couldnt connect to database after 100 seconds

    """
    log.debug("CONNECTING TO DATABASE (LOCAL TEST)")
    wait_time = 0
    timeout = TEST_TIMEOUT
    while wait_time < timeout:
        try:
            db = SqliteDatabase(LOCAL_SQLITE_FILENAME)
            break

        except OperationalError: 
            log.info("Waiting for database")
            time.sleep(5)
            wait_time += 5
    
    if wait_time > timeout: 
        log.error("Failed to connect to (local) database")
        raise TimeoutError("Database connection attempts timed out")

    log.info("CONNECTED TO DATABASE (LOCAL TEST)")

    return db


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
        password=os.environ.get("SESSION_PASS")
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
