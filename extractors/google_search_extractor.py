import math
import re
import time

import requests
from bs4 import BeautifulSoup

from extractors.base_extractor import BaseExtractor
from config.settings import (
    GOOGLE_SEARCH_DELAY,
    GOOGLE_SEARCH_TIMEOUT,
)


# Lista fillestare e aftesive qe do te kerkohen ne Google.
SEED_SKILLS = [
    "python",
    "javascript",
    "java",
    "sql",
    "docker",
    "kubernetes",
    "react",
    "aws",
    "machine learning",
    "git",
    "typescript",
    "linux",
    "django",
    "node.js",
    "postgresql",
]


class GoogleSearchExtractor(BaseExtractor):
    source_name = "google_search"

    SEARCH_URL = "https://www.google.com/search"

    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/126.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
    }

    @staticmethod
    def _parse_result_count(html):
        """
        Nxjerr numrin e rezultateve nga teksti:
        'About 1,230,000 results'
        """
        soup = BeautifulSoup(html, "html.parser")
        result_stats = soup.select_one("#result-stats")

        if result_stats is None:
            return None

        result_text = result_stats.get_text(" ", strip=True)

        match = re.search(
            r"([\d,.\s]+)\s+results",
            result_text,
            flags=re.IGNORECASE,
        )

        if match is None:
            return None

        digits_only = re.sub(r"\D", "", match.group(1))

        if not digits_only:
            return None

        return int(digits_only)

    def _search_skill(self, session, skill):
        """
        Kerkon skill-in ne kontekstin e vendeve te punes.
        """
        params = {
            "q": f'"{skill}" jobs',
            "hl": "en",
            "pws": "0",
            "filter": "0",
        }

        response = session.get(
            self.SEARCH_URL,
            params=params,
            timeout=GOOGLE_SEARCH_TIMEOUT,
        )

        if response.status_code == 429:
            raise RuntimeError(
                "Google Search bllokoi kerkesat me statusin 429."
            )

        response.raise_for_status()

        response_text = response.text.lower()

        if "unusual traffic" in response_text:
            raise RuntimeError(
                "Google Search identifikoi trafik automatik."
            )

        return self._parse_result_count(response.text)

    @staticmethod
    def _calculate_interest_scores(results):
        """
        Normalizon numrin e rezultateve ne nje interest_score
        nga 0 deri ne 100.

        Perdor shkalle logaritmike sepse numri i rezultateve
        mund te ndryshoje shume midis skills.
        """
        valid_results = [
            result
            for result in results
            if result["result_count"] is not None
        ]

        if not valid_results:
            return results

        log_counts = [
            math.log1p(result["result_count"])
            for result in valid_results
        ]

        minimum = min(log_counts)
        maximum = max(log_counts)

        for result, log_count in zip(valid_results, log_counts):
            if minimum == maximum:
                score = 100.0
            else:
                score = (
                    (log_count - minimum)
                    / (maximum - minimum)
                ) * 100

            result["interest_score"] = round(score, 2)

        return results

    def extract(self):
        results = []

        session = requests.Session()
        session.headers.update(self.HEADERS)

        for index, skill in enumerate(SEED_SKILLS):
            try:
                result_count = self._search_skill(
                    session=session,
                    skill=skill,
                )

                results.append({
                    "skill": skill,
                    "result_count": result_count,
                    "interest_score": None,
                })

            except requests.RequestException as error:
                print(
                    f"Google Search request failed for "
                    f"'{skill}': {error}"
                )

                results.append({
                    "skill": skill,
                    "result_count": None,
                    "interest_score": None,
                })

            except RuntimeError as error:
                print(f"Google Search extraction stopped: {error}")
                break

            # Nuk ben pause pas skill-it te fundit.
            if index < len(SEED_SKILLS) - 1:
                time.sleep(GOOGLE_SEARCH_DELAY)

        session.close()

        return self._calculate_interest_scores(results)


# Teston vetem kete extractor pa ekzekutuar pipeline-in e plote.
if __name__ == "__main__":
    extractor = GoogleSearchExtractor()
    extractor.run()