import contextlib
import os
import sqlite3

DB = os.getenv("WG_MONITOR_DB", "../db.sqlite3")


@contextlib.contextmanager
def get_connection():
    con = sqlite3.connect(DB)

    try:
        yield con
        con.commit()
    finally:
        con.close()
