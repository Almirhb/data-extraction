from config.settings import validate_config

from extractors.remoteok_extractor import RemoteOKExtractor
from extractors.github_extractor import GitHubExtractor
from extractors.stackoverflow_extractor import StackOverflowExtractor
from extractors.trends_extractor import TrendsExtractor

from storage.raw_staging import get_connection as get_raw_connection, get_records_by_source
from storage.pipeline_db import (
    get_connection as get_pipeline_connection,
    create_tables,
    insert_or_get_skill,
    insert_skill_metric,
)

from transformers.data_cleaner import clean_raw_records
from analysis.roi_calculator import calculate_roi_scores
from analysis.report_generator import generate_report

# google_search_extractor left out for now, still unreliable (Google blocks scraping)
EXTRACTORS = [RemoteOKExtractor, GitHubExtractor, StackOverflowExtractor, TrendsExtractor]


def run_extractors():
    """Step 1: pull raw data from every source and save it into raw_staging.db"""
    print("Running extractors...")
    for extractor_class in EXTRACTORS:
        extractor = extractor_class()
        extractor.run()


def run_transform_and_load():
    """
    Step 2: read raw records back out, clean/normalize them, and count how
    many times each skill shows up per source. Save those counts into
    pipeline.db as SkillMetrics.
    """
    print("Transforming and loading data...")

    raw_conn = get_raw_connection()
    pipeline_conn = get_pipeline_connection()
    create_tables(pipeline_conn)

    for extractor_class in EXTRACTORS:
        source = extractor_class.source_name
        raw_records = get_records_by_source(raw_conn, source)
        cleaned = clean_raw_records(raw_records)

        # tally up how many times each skill appears for this source
        skill_counts = {}

        for src, cleaned_data in cleaned:
            if isinstance(cleaned_data, list):
                # remoteok/github give us a list of skills per record,
                # count how many times each one shows up
                for skill in cleaned_data:
                    skill_counts[skill] = skill_counts.get(skill, 0) + 1

            elif isinstance(cleaned_data, dict):
                # stackoverflow/trends already come as one skill + a count/score
                skill = cleaned_data.get("skill")
                value = cleaned_data.get("count") or cleaned_data.get("score") or 0
                if skill:
                    skill_counts[skill] = skill_counts.get(skill, 0) + value

        for skill_name, count in skill_counts.items():
            skill_id = insert_or_get_skill(pipeline_conn, skill_name)
            insert_skill_metric(pipeline_conn, skill_id, source, count)

    raw_conn.close()
    pipeline_conn.close()


def run_analysis():
    """Step 3: calculate ROI scores and generate the final report"""
    print("Running analysis...")

    conn = get_pipeline_connection()
    calculate_roi_scores(conn)
    generate_report(conn)
    conn.close()


def run_pipeline():
    """Runs the whole thing, start to finish. This is what main.py calls."""
    validate_config()

    run_extractors()
    run_transform_and_load()
    run_analysis()

    print("Pipeline finished.")