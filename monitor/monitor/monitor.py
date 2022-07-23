import logging

from .db import get_connection

logger = logging.getLogger(__name__)


def create_monitor_tables():
    logger.info("Creating monitoring table if not exists")
    with get_connection() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS "monitor" (
            "public_key" varchar(255),
            "receive_bytes" bigint,
            "transmit_bytes" bigint,
            "ts" datetime
        )
        """)
        conn.execute("""
        CREATE INDEX IF NOT EXISTS monitor_ts ON "monitor" ("ts")
        """)


def make_measure():
    logger.info("Making a measure")

    with get_connection() as con:
        con.execute("""
        INSERT INTO "monitor" (
            "public_key",
            "receive_bytes",
            "transmit_bytes",
            "ts"
        )
        SELECT
            "public_key",
            "receive_bytes",
            "transmit_bytes",
            CURRENT_TIMESTAMP
        FROM "devices"
        WHERE "last_handshake_time" > datetime(CURRENT_TIMESTAMP, '-5 minutes')
        """)


def cleanup():

    logger.info("Performing cleanup")

    with get_connection() as con:
        con.execute("""
        DELETE FROM "monitor"
        WHERE "last_handshake_time" < datetime(CURRENT_TIMESTAMP, '-7 days')
        """)
