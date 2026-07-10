import requests

from extractors.base_extractor import BaseExtractor
from config.settings import STACKEXCHANGE_KEY

STACKEXCHANGE_TAGS_URL = "https://api.stackexchange.com/2.3/tags"

# how many pages of tags to pull, 100 tags per page is the API max
PAGE_SIZE = 100
PAGES_TO_FETCH = 3


class StackOverflowExtractor(BaseExtractor):
    source_name = "stackoverflow"

    def extract(self):
        results = []

        for page in range(1, PAGES_TO_FETCH + 1):
            params = {
                "order": "desc",
                "sort": "popular",
                "site": "stackoverflow",
                "pagesize": PAGE_SIZE,
                "page": page,
            }

            # key is optional, without it we just get a lower rate limit
            if STACKEXCHANGE_KEY:
                params["key"] = STACKEXCHANGE_KEY

            response = requests.get(STACKEXCHANGE_TAGS_URL, params=params)
            response.raise_for_status()

            data = response.json()

            for tag in data.get("items", []):
                results.append({
                    "tag": tag.get("name"),
                    "count": tag.get("count"),
                })

            # no more pages left, stop early
            if not data.get("has_more"):
                break

        return results


# quick way to test just this extractor without running the full pipeline
if __name__ == "__main__":
    extractor = StackOverflowExtractor()
    extractor.run()