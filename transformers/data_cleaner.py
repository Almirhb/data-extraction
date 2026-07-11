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
    """
    tag = raw_data.get("tag")
    count = raw_data.get("count", 0)

    return {
        "skill": normalize_skill_list([tag])[0] if tag else None,
        "count": count,
    }


def clean_trends_record(raw_data: dict) -> dict:
    """
    Trends records already come as one skill + score, just normalize the name.
    """
    skill = raw_data.get("skill")
    score = raw_data.get("interest_score", 0)

    return {
        "skill": normalize_skill_list([skill])[0] if skill else None,
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