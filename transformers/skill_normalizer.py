# maps common aliases/variations to one standard name
SKILL_ALIASES = {
    "js": "javascript",
    "ts": "typescript",
    "py": "python",
    "ml": "machine learning",
    "ai": "artificial intelligence",
    "k8s": "kubernetes",
    "postgres": "postgresql",
    "node": "node.js",
    "nodejs": "node.js",
    "reactjs": "react",
    "react.js": "react",
    "vuejs": "vue",
    "vue.js": "vue",
    "golang": "go",
    "csharp": "c#",
}

# whitelist of recognized technical skills - languages, frameworks, tools,
# platforms, databases, concepts. instead of trying to blacklist every
# possible non-skill tag (impossible to keep up with), we only accept
# tags that are actually on this list.
#
# this list will need to grow as new relevant skills show up, that's
# expected and fine - safer to miss a skill than to include job-category noise
KNOWN_SKILLS = {
    # languages
    "python", "javascript", "typescript", "java", "c#", "c++", "c",
    "go", "rust", "ruby", "php", "swift", "kotlin", "scala", "r",
    "sql", "html", "css", "bash", "shell",

    # frontend
    "react", "vue", "angular", "svelte", "next.js", "tailwind",

    # backend / frameworks
    "django", "flask", "fastapi", "node.js", "express", "spring",
    "rails", "laravel", "asp.net",

    # databases
    "postgresql", "mysql", "mongodb", "redis", "sqlite", "elasticsearch",
    "dynamodb", "cassandra",

    # cloud / devops
    "aws", "azure", "gcp", "docker", "kubernetes", "terraform",
    "jenkins", "ci/cd", "linux", "nginx",

    # data / ai
    "machine learning", "artificial intelligence", "deep learning",
    "data science", "pandas", "numpy", "tensorflow", "pytorch",
    "nlp", "computer vision",

    # other common tech tools/concepts
    "git", "graphql", "rest api", "microservices", "api",
    "cybersecurity", "infosec", "blockchain", "devops",
}


def is_valid_skill(name: str) -> bool:
    """
    Only accept tags that are known technical skills.
    This is a whitelist approach - safer than trying to blacklist every
    possible non-skill category, since new noise tags show up constantly.
    """
    return name in KNOWN_SKILLS


def normalize_skill_name(raw_name: str) -> str:
    """
    Takes a raw skill name (from tags, topics, job titles, whatever)
    and returns a clean, standardized version.
    """
    if not raw_name:
        return ""

    name = raw_name.strip().lower()

    if name in SKILL_ALIASES:
        name = SKILL_ALIASES[name]

    return name


def normalize_skill_list(raw_names: list) -> list:
    """
    Same as above but for a whole list at once, also filters out
    anything that isn't a recognized skill, and removes duplicates.
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