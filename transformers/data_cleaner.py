import json

from transformers.skill_normalizer import normalize_skill_list


def clean_remoteok_record(raw_data: dict) -> list:
    """
    RemoteOK records have a "tags" list which is basically our skills.
    Returns a normalized list of skill names found in this one job posting.
    """
    tags = raw_data.get("tags", [])
    return normalize_skill_list(tags)


def clean_github_record(raw_data: dict) -> list:
    """
    GitHub records have "topics" (tags on the repo) plus a "language" field.
    Combine both into one list of skills for this repo.
    """
    topics = raw_data.get("topics", [])
    language = raw_data.get("language")

    skills = list(topics)
    if language:
        skills.append(language)

    return normalize_skill_list(skills)


def clean_stackoverflow_record(raw_data: dict) -> dict:
    """
    StackOverflow records are already one skill per record (the tag itself),
    with a count. Just normalize the tag name.

    Note: normalize_skill_list() now filters against a whitelist of known
    skills, so most tags (which aren't tech skills, or aren't on our list
    yet) will come back as an empty list. That's expected - we just end up
    with skill=None for those, and the orchestrator skips None skills.
    """
    tag = raw_data.get("tag")
    count = raw_data.get("count", 0)

    normalized = normalize_skill_list([tag]) if tag else []
    skill = normalized[0] if normalized else None

    return {
        "skill": skill,
        "count": count,
    }


def clean_trends_record(raw_data: dict) -> dict:
    """
    Trends records already come as one skill + score, just normalize the name.
    Same empty-list handling as clean_stackoverflow_record above.
    """
    skill_raw = raw_data.get("skill")
    score = raw_data.get("interest_score", 0)

    normalized = normalize_skill_list([skill_raw]) if skill_raw else []
    skill = normalized[0] if normalized else None

    return {
        "skill": skill,
        "score": score,
    }


# maps source name -> the right cleaning function for that source's raw shape
CLEANERS = {
    "remoteok": clean_remoteok_record,
    "github": clean_github_record,
    "stackoverflow": clean_stackoverflow_record,
    "trends": clean_trends_record,
}


def clean_raw_records(raw_records: list) -> list:
    """
    Takes rows straight from raw_staging.db (id, source, raw_data_json, fetched_at)
    and runs each one through the right cleaner based on its source.

    Returns a list of (source, cleaned_data) tuples, skipping sources we
    don't have a cleaner for yet.
    """
    results = []

    for row in raw_records:
        _, source, raw_data_json, _ = row
        raw_data = json.loads(raw_data_json)

        cleaner = CLEANERS.get(source)
        if not cleaner:
            continue

        cleaned = cleaner(raw_data)
        results.append((source, cleaned))

    return results