"""
extractors/base_extractor.py

Abstract base class that all concrete extractors must inherit from.
Guarantees every extractor exposes the same interface, so the orchestrator
can call them interchangeably without knowing the specifics of each source.

Usage:
    class RemoteOKExtractor(BaseExtractor):
        def extract(self):
            # fetch data, return a list of dicts
            ...
"""

from abc import ABC, abstractmethod

from storage.raw_staging import get_connection, create_tables, insert_raw_record


class BaseExtractor(ABC):
    """
    Base class for all data extractors.

    Each subclass must implement extract(), which fetches data from its
    specific source and returns it as a list of dictionaries (raw, unprocessed).

    The base class handles the common part: saving whatever extract() returns
    into the raw_staging database, tagged with the source name.
    """

    #: Must be overridden by each subclass, e.g. "remoteok", "github"
    source_name: str = None

    def __init__(self):
        if not self.source_name:
            raise ValueError(
                f"{self.__class__.__name__} must define a 'source_name' class attribute."
            )

    @abstractmethod
    def extract(self) -> list[dict]:
        """
        Fetch raw data from the external source.

        Returns:
            A list of dictionaries, one per record. The structure of each
            dict is source-specific — transformers will normalize it later.
        """
        raise NotImplementedError

    def run(self):
        """
        Runs the full extraction step: calls extract(), then saves every
        returned record into raw_staging.db.
        """
        records = self.extract()

        conn = get_connection()
        create_tables(conn)

        for record in records:
            insert_raw_record(conn, source=self.source_name, raw_data=record)

        conn.close()

        print(f"[{self.source_name}] Saved {len(records)} raw records.")
        return len(records)