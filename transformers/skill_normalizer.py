# maps common aliases/variations to one standard name
# this list will grow over time as we see more raw data come through
SKILL_ALIASES = {
    "js": "javascript",
    "ts": "typescript",
    "py": "python",
    "ml": "machine learning",
    "k8s": "kubernetes",
    "postgres": "postgresql",
    "node": "node.js",
    "nodejs": "node.js",
    "reactjs": "react",
    "react.js": "react",
}


def normalize_skill_name(raw_name: str) -> str:
    """
    Takes a raw skill name (from tags, topics, job titles, whatever)
    and returns a clean, standardized version.
    """
    if not raw_name:
        return ""

    name = raw_name.strip().lower()

    # collapse variations we know about
    if name in SKILL_ALIASES:
        name = SKILL_ALIASES[name]

    return name


def normalize_skill_list(raw_names: list) -> list:
    """
    Same as above but for a whole list at once, also removes empty
    strings and duplicates that appear after normalization.
    """
    normalized = [normalize_skill_name(name) for name in raw_names]
    normalized = [name for name in normalized if name]

    # dedupe while keeping order (set() alone would shuffle things)
    seen = set()
    result = []
    for name in normalized:
        if name not in seen:
            seen.add(name)
            result.append(name)

    return result