from transformers.data_cleaner import (
    clean_remoteok_record,
    clean_github_record,
    clean_stackoverflow_record,
    clean_trends_record,
)


def test_clean_remoteok_record_extracts_tags():
    raw = {"title": "Python Developer", "tags": ["Python", "Django", "SQL"]}
    result = clean_remoteok_record(raw)

    assert result == ["python", "django", "sql"]


def test_clean_remoteok_record_handles_missing_tags():
    raw = {"title": "Some Job"}
    result = clean_remoteok_record(raw)

    assert result == []


def test_clean_github_record_combines_topics_and_language():
    raw = {"topics": ["web", "api"], "language": "Python"}
    result = clean_github_record(raw)

    assert "python" in result
    assert "web" in result
    assert "api" in result


def test_clean_github_record_handles_no_language():
    raw = {"topics": ["docker"], "language": None}
    result = clean_github_record(raw)

    assert result == ["docker"]


def test_clean_stackoverflow_record():
    raw = {"tag": "python", "count": 500}
    result = clean_stackoverflow_record(raw)

    assert result == {"skill": "python", "count": 500}


def test_clean_trends_record():
    raw = {"skill": "docker", "interest_score": 42.5}
    result = clean_trends_record(raw)

    assert result == {"skill": "docker", "score": 42.5}