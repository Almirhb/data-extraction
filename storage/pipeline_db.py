"""
storage/pipeline_db.py

Menaxhon databazen pipeline.db - ku ruhen te dhenat e perpunuara:
skills e normalizuara, metrics per burim, dhe ROI scores finale.

Perdorim ne transformers/analysis:
    from storage.pipeline_db import get_connection, create_tables, insert_or_get_skill

    conn = get_connection()
    create_tables(conn)
    skill_id = insert_or_get_skill(conn, "Python")
"""

import sqlite3
from datetime import datetime

from config.settings import PIPELINE_DB_PATH
from storage.models import PIPELINE_TABLES


def get_connection():
    """
    Hap nje lidhje te re me pipeline.db.
    Cdo modul qe e perdor duhet te therrase conn.close() kur mbaron.
    """
    conn = sqlite3.connect(PIPELINE_DB_PATH)
    return conn


def create_tables(conn):
    """
    Krijon te gjitha tabelat e pipeline.db (Skills, SkillMetrics, ROIScores)
    nese s'ekzistojne ende. Renditja eshte e rendesishme per shkak te foreign keys.
    """
    cur = conn.cursor()
    for table_schema in PIPELINE_TABLES:
        cur.execute(table_schema)
    conn.commit()


def insert_or_get_skill(conn, name: str) -> int:
    """
    Fut nje skill te ri nese s'ekziston, ose kthen id-ne e atij ekzistues.
    Perdor INSERT OR IGNORE per te shmangur duplikatet (name eshte UNIQUE).

    Args:
        conn: lidhja sqlite3
        name: emri i normalizuar i skillit, p.sh. "python", "docker"

    Returns:
        id i skillit ne tabelen Skills
    """
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO Skills (name) VALUES (?)", (name,))
    conn.commit()

    cur.execute("SELECT id FROM Skills WHERE name = ?", (name,))
    row = cur.fetchone()
    return row[0]


def insert_skill_metric(conn, skill_id: int, source: str, demand_count: int):
    """
    Ruan nje metrike per nje skill nga nje burim i caktuar
    (p.sh. sa here u perket "Python" ne RemoteOK sot).
    """
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO SkillMetrics (skill_id, source, demand_count, collected_at) VALUES (?, ?, ?, ?)",
        (skill_id, source, demand_count, datetime.now().isoformat())
    )
    conn.commit()


def upsert_roi_score(conn, skill_id: int, roi_score: float):
    """
    Fut ose perditeson ROI score-in per nje skill.
    Nese skill_id ekziston tashme ne ROIScores, e perditeson (skill_id eshte UNIQUE).
    """
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO ROIScores (skill_id, roi_score, calculated_at)
        VALUES (?, ?, ?)
        ON CONFLICT(skill_id) DO UPDATE SET
            roi_score = excluded.roi_score,
            calculated_at = excluded.calculated_at
        """,
        (skill_id, roi_score, datetime.now().isoformat())
    )
    conn.commit()


def get_all_skills_with_roi(conn):
    """
    Kthen te gjitha skills bashke me ROI score-in e tyre (per report_generator).

    Returns:
        Liste tuplesh (skill_name, roi_score)
    """
    cur = conn.cursor()
    cur.execute(
        """
        SELECT Skills.name, ROIScores.roi_score
        FROM Skills
        JOIN ROIScores ON Skills.id = ROIScores.skill_id
        ORDER BY ROIScores.roi_score DESC
        """
    )
    return cur.fetchall()