#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SQL connectors

Connectors for both remote and local SQL based databases

Currently Supported: 
    Local: 
        - SQLite
    Remote: 
        - Postgres

"""
import os
import time
import structlog

from peewee import OperationalError
from playhouse.db_url import connect
from peewee import SqliteDatabase

log = structlog.get_logger(__name__)

LOCAL_SQLITE_FILENAME = "test.db"
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
            db = connect(
                "postgresql://{}:{}@{}:{}/{}".format(
                    os.environ.get("DB_USER"),
                    os.environ.get("DB_PASS"),
                    os.environ.get("DB_HOST"),
                    os.environ.get("DB_PORT"),
                    os.environ.get("DB_NAME"),
                )
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
