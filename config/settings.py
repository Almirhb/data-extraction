"""
config/settings.py

main configuration of projects. read variables from  .env and put them as constant for
(extractors, storage, analysis, etj.).

used in others module
    from config.settings import GITHUB_TOKEN, PIPELINE_DB_PATH
"""

import os
from dotenv import load_dotenv

# Ngarkon variablat nga .env ne mjedisin e Python-it
load_dotenv()

# --- GitHub API ---
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# --- StackExchange API ---
STACKEXCHANGE_KEY = os.getenv("STACKEXCHANGE_KEY")

# --- Database paths ---
RAW_STAGING_DB_PATH = os.getenv("RAW_STAGING_DB_PATH", "data/raw_staging.db")
PIPELINE_DB_PATH = os.getenv("PIPELINE_DB_PATH", "data/pipeline.db")

# --- Logging ---
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE_PATH = os.getenv("LOG_FILE_PATH", "logs/pipeline.log")

GOOGLE_SEARCH_TIMEOUT = 15
GOOGLE_SEARCH_DELAY = 3


def validate_config():
    """
    control of variables
    """
    missing = []

    if not GITHUB_TOKEN:
        missing.append("GITHUB_TOKEN")

    if missing:
        raise EnvironmentError(
            f"variable are missing in environment of .env: {', '.join(missing)}. "
            f"look .env.example for reference."
        )