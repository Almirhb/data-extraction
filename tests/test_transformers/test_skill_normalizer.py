from transformers.skill_normalizer import normalize_skill_name, normalize_skill_list


def test_normalize_lowercases_and_strips():
    assert normalize_skill_name("  Python  ") == "python"


def test_normalize_applies_known_alias():
    assert normalize_skill_name("JS") == "javascript"
    assert normalize_skill_name("k8s") == "kubernetes"


def test_normalize_handles_empty_input():
    assert normalize_skill_name("") == ""
    assert normalize_skill_name(None) == ""


def test_normalize_list_removes_duplicates_after_normalization():
    # "JS" and "js" and "javascript" should all collapse into one entry
    raw = ["JS", "js", "JavaScript", "python"]
    result = normalize_skill_list(raw)

    assert result.count("javascript") == 1
    assert "python" in result


def test_normalize_list_keeps_order():
    raw = ["python", "docker", "react"]
    result = normalize_skill_list(raw)

    assert result == ["python", "docker", "react"]


def test_normalize_list_drops_empty_strings():
    raw = ["python", "", None, "docker"]
    result = normalize_skill_list(raw)

    assert result == ["python", "docker"]