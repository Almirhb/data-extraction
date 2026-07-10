"""
storage/models.py

Perkufizimet e skemave SQL per te dyja databazat e projektit.
Ky file s'ka logjike, vetem struktura e tabelave (CREATE TABLE statements).

raw_staging.db  -> ruan te dhenat raw, ashtu si vijne nga extractors, para pastrimit
pipeline.db     -> ruan te dhenat e perpunuara: skills, metrics per burim, ROI scores
"""

# ============================================
# RAW STAGING SCHEMA
# ============================================

RAW_STAGING_SCHEMA = """
CREATE TABLE IF NOT EXISTS RawRecords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT NOT NULL,
    raw_data TEXT NOT NULL,
    fetched_at TEXT NOT NULL
)
"""

# ============================================
# PIPELINE SCHEMA
# ============================================

SKILLS_TABLE = """
CREATE TABLE IF NOT EXISTS Skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
)
"""

SKILL_METRICS_TABLE = """
CREATE TABLE IF NOT EXISTS SkillMetrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    skill_id INTEGER NOT NULL,
    source TEXT NOT NULL,
    demand_count INTEGER NOT NULL,
    collected_at TEXT NOT NULL,
    FOREIGN KEY (skill_id) REFERENCES Skills(id)
)
"""

ROI_SCORES_TABLE = """
CREATE TABLE IF NOT EXISTS ROIScores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    skill_id INTEGER NOT NULL UNIQUE,
    roi_score REAL NOT NULL,
    calculated_at TEXT NOT NULL,
    FOREIGN KEY (skill_id) REFERENCES Skills(id)
)
"""

# Lista e te gjitha tabelave te pipeline.db, ne renditjen qe duhen krijuar
# (Skills para SkillMetrics/ROIScores, per shkak te foreign keys)
PIPELINE_TABLES = [SKILLS_TABLE, SKILL_METRICS_TABLE, ROI_SCORES_TABLE]