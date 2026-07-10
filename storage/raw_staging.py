"""
storage/raw_staging.py

Menaxhon databazen raw_staging.db - ku ruhen te dhenat "te papregatitura",
pikerisht ashtu si vijne nga extractors, para se transformers t'i pastrojne.

Perdorim ne extractors:
    from storage.raw_staging import get_connection, create_tables, insert_raw_record

    conn = get_connection()
    create_tables(conn)
    insert_raw_record(conn, source="remoteok", raw_data={"title": "Python Dev", ...})
"""

import sqlite3
import json
from datetime import datetime

from config.settings import RAW_STAGING_DB_PATH
from storage.models import RAW_STAGING_SCHEMA


def get_connection():
    """
    Hap nje lidhje te re me raw_staging.db.
    Cdo modul qe e perdor duhet te therrase conn.close() kur mbaron.
    """
    conn = sqlite3.connect(RAW_STAGING_DB_PATH)
    return conn


def create_tables(conn):
    """
    Krijon tabelen RawRecords nese s'ekziston ende.
    E sigurte per t'u thirrur shume here (CREATE TABLE IF NOT EXISTS).
    """
    cur = conn.cursor()
    cur.execute(RAW_STAGING_SCHEMA)
    conn.commit()


def insert_raw_record(conn, source: str, raw_data: dict):
    """
    Ruan nje rekord raw ne databaze.

    Args:
        conn: lidhja sqlite3 (nga get_connection)
        source: emri i burimit, p.sh. "remoteok", "github", "stackoverflow"
        raw_data: dictionary me te dhenat raw, ruhet si JSON string
    """
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO RawRecords (source, raw_data, fetched_at) VALUES (?, ?, ?)",
        (source, json.dumps(raw_data), datetime.now().isoformat())
    )
    conn.commit()


def get_records_by_source(conn, source: str):
    """
    Kthen te gjitha rekordet raw per nje burim te caktuar.
    Perdoret nga transformers per te lexuar te dhenat qe do pastrohen.

    Returns:
        Liste tuplesh (id, source, raw_data_json_string, fetched_at)
    """
    cur = conn.cursor()
    cur.execute("SELECT id, source, raw_data, fetched_at FROM RawRecords WHERE source = ?", (source,))
    return cur.fetchall()