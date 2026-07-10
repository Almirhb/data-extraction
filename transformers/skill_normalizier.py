import re
import unicodedata


SKILL_ALIASES = {
    # Python
    "python 3": "python",
    "python3": "python",
    "python programming": "python",

    # JavaScript
    "js": "javascript",
    "java script": "javascript",
    "javascript programming": "javascript",
    "ecmascript": "javascript",

    # TypeScript
    "ts": "typescript",
    "type script": "typescript",

    # Java
    "java programming": "java",
    "java se": "java",
    "java ee": "java",
    "jakarta ee": "java",

    # SQL
    "structured query language": "sql",
    "sql language": "sql",

    # PostgreSQL
    "postgres": "postgresql",
    "postgre sql": "postgresql",
    "postgre": "postgresql",

    # Node.js
    "node": "node.js",
    "nodejs": "node.js",
    "node js": "node.js",
    "node-js": "node.js",

    # React
    "reactjs": "react",
    "react js": "react",
    "react.js": "react",

    # Django
    "django framework": "django",
    "python django": "django",

    # Docker
    "docker containers": "docker",
    "docker container": "docker",

    # Kubernetes
    "k8s": "kubernetes",
    "kube": "kubernetes",

    # Machine learning
    "ml": "machine learning",
    "machine-learning": "machine learning",
    "machinelearning": "machine learning",

    # Artificial intelligence
    "ai": "artificial intelligence",
    "artificial-intelligence": "artificial intelligence",

    # AWS
    "amazon web services": "aws",
    "amazon aws": "aws",
    "aws cloud": "aws",

    # Azure
    "microsoft azure": "azure",
    "azure cloud": "azure",

    # Google Cloud
    "google cloud platform": "gcp",
    "google cloud": "gcp",

    # Git
    "git version control": "git",
    "git scm": "git",

    # Linux
    "gnu linux": "linux",
    "linux operating system": "linux",

    # C#
    "c sharp": "c#",
    "c-sharp": "c#",
    "csharp": "c#",

    # C++
    "c plus plus": "c++",
    "cplusplus": "c++",

    # .NET
    "dotnet": ".net",
    "dot net": ".net",
    "microsoft .net": ".net",

    # MongoDB
    "mongo": "mongodb",
    "mongo db": "mongodb",

    # MySQL
    "my sql": "mysql",

    # HTML
    "html5": "html",

    # CSS
    "css3": "css",

    # Vue
    "vuejs": "vue.js",
    "vue js": "vue.js",
    "vue": "vue.js",

    # Angular
    "angularjs": "angular",
    "angular js": "angular",

    # Next.js
    "nextjs": "next.js",
    "next js": "next.js",

    # Express
    "expressjs": "express.js",
    "express js": "express.js",
    "express": "express.js",

    # Scikit-learn
    "sklearn": "scikit-learn",
    "scikit learn": "scikit-learn",

    # TensorFlow
    "tensor flow": "tensorflow",

    # PyTorch
    "py torch": "pytorch",

    # Power BI
    "powerbi": "power bi",

    # REST API
    "rest api": "rest",
    "restful api": "rest",
    "restful services": "rest",
}


class SkillNormalizer:
    """
    Converts skill aliases into one canonical skill name.
    """

    @staticmethod
    def _prepare_skill(skill: str) -> str:
        """
        Applies basic formatting before alias matching.
        """
        skill = unicodedata.normalize("NFKC", skill)
        skill = skill.strip().lower()

        skill = skill.replace("_", " ")
        skill = re.sub(r"\s+", " ", skill)

        return skill

    def normalize_skill(self, skill: str | None) -> str | None:
        """
        Normalizes one skill name.
        """
        if not isinstance(skill, str):
            return None

        prepared_skill = self._prepare_skill(skill)

        if not prepared_skill:
            return None

        if prepared_skill in SKILL_ALIASES:
            return SKILL_ALIASES[prepared_skill]

        return prepared_skill

    def transform(self, records: list[dict] | None) -> list[dict]:
        """
        Normalizes the skill field in every record.
        """
        if not records:
            return []

        normalized_records = []

        for record in records:
            if not isinstance(record, dict):
                continue

            normalized_skill = self.normalize_skill(
                record.get("skill")
            )

            if normalized_skill is None:
                continue

            normalized_record = record.copy()
            normalized_record["skill"] = normalized_skill

            normalized_records.append(normalized_record)

        return normalized_records


if __name__ == "__main__":
    sample_data = [
        {"skill": "Python3", "interest_score": 95},
        {"skill": "JS", "interest_score": 80},
        {"skill": "NodeJS", "interest_score": 75},
        {"skill": "K8s", "interest_score": 70},
        {"skill": "Amazon Web Services", "interest_score": 85},
    ]

    normalizer = SkillNormalizer()
    normalized_data = normalizer.transform(sample_data)

    for item in normalized_data:
        print(item)