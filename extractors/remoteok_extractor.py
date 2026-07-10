import requests

from extractors.base_extractor import BaseExtractor

# RemoteOK has a public API that returns JSON, no token needed
REMOTEOK_API_URL = "https://remoteok.com/api"


class RemoteOKExtractor(BaseExtractor):
    source_name = "remoteok"

    def extract(self):
        # User-Agent header is required, RemoteOK rejects requests without it
        headers = {"User-Agent": "Mozilla/5.0"}

        response = requests.get(REMOTEOK_API_URL, headers=headers)
        response.raise_for_status()

        data = response.json()

        # the first item in the list is always a "legal notice", not a job
        # that's just how RemoteOK's API works, so we drop it
        jobs = data[1:]

        results = []
        for job in jobs:
            results.append({
                "title": job.get("position"),
                "company": job.get("company"),
                "tags": job.get("tags", []),
                "date": job.get("date"),
                "url": job.get("url"),
            })

        return results


# quick way to test just this extractor without running the full pipeline
if __name__ == "__main__":
    extractor = RemoteOKExtractor()
    extractor.run()