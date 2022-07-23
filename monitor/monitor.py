import datetime
import contextlib
import logging
import os
import sqlite3
import time

logger = logging.getLogger(__name__)
DB = os.getenv("WG_MONITOR_DB", "./db.sqlite3")


@contextlib.contextmanager
def get_cursor():
    con = sqlite3.connect(DB)

    try:
        cursor = con.cursor()
        yield cursor
        con.commit()
    finally:
        con.close()


def create_monitor_tables():
    logger.info("Creating monitoring table if not exists")
    with get_cursor() as cursor:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS "monitor" (
            "public_key" varchar(255),
            "is_connected" boolean,
            "receive_bytes" bigint,
            "transmit_bytes" bigint,
            "ts" datetime
        )""")


def make_measure():
    logger.info("Making a measure")

    with get_cursor() as cursor:
        cursor.execute("""
        INSERT INTO "monitor" (
            "public_key",
            "is_connected",
            "receive_bytes",
            "transmit_bytes",
            "ts"
        )
        SELECT
            "public_key",
            "last_handshake_time" > datetime(CURRENT_TIMESTAMP, '-5 minutes'),
            "receive_bytes",
            "transmit_bytes",
            CURRENT_TIMESTAMP
        FROM "devices"
        """)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    create_monitor_tables()
    make_measure()
