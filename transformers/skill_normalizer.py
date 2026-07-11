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

# tags that show up in job postings but aren't actual technical skills -
# job categories, employment types, department names, etc.
# RemoteOK especially mixes these in with real skill tags, so we filter them out
NON_SKILL_TAGS = {
    "full-time", "part-time", "contract", "freelance", "remote",
    "exec", "executive", "senior", "junior", "lead", "intern", "internship",
    "customer support", "customer service", "marketing", "sales",
    "finance", "accounting", "hr", "human resources", "legal",
    "education", "teaching", "medical", "healthcare",
    "ops", "operations", "management", "admin", "administrative",
    "content writing", "copywriting", "writing",
    "digital nomad", "travel",
    "non tech", "no experience",
}


def is_valid_skill(name: str) -> bool:
    """
    Returns False for tags that are job categories/employment info
    rather than actual technical skills.
    """
    return name not in NON_SKILL_TAGS


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
    strings, non-skill tags, and duplicates that appear after normalization.
    """
    normalized = [normalize_skill_name(name) for name in raw_names]
    normalized = [name for name in normalized if name and is_valid_skill(name)]

    # dedupe while keeping order (set() alone would shuffle things)
    seen = set()
    result = []
    for name in normalized:
        if name not in seen:
            seen.add(name)
            result.append(name)

    return result