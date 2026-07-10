from github import Github

from extractors.base_extractor import BaseExtractor
from config.settings import GITHUB_TOKEN

# how many repos to pull, more repos = better signal but slower + uses more API calls
REPO_LIMIT = 50


class GitHubExtractor(BaseExtractor):
    source_name = "github"

    def extract(self):
        client = Github(GITHUB_TOKEN)

        # sorted by stars, only repos with decent traction so we don't get noise
        repos = client.search_repositories(query="stars:>1000", sort="stars", order="desc")

        results = []
        for i, repo in enumerate(repos):
            if i >= REPO_LIMIT:
                break

            results.append({
                "name": repo.full_name,
                "language": repo.language,
                "topics": repo.get_topics(),
                "stars": repo.stargazers_count,
                "url": repo.html_url,
            })

        return results


# quick way to test just this extractor without running the full pipeline
if __name__ == "__main__":
    extractor = GitHubExtractor()
    extractor.run()