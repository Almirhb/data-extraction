import json
import re
from typing import Any


class DataCleaner:
    """
    Cleans extracted records before skill normalization.

    Expected input:
    [
        {
            "skill": " Python ",
            "interest_score": "85.4",
            "result_count": "1,200,000",
        }
    ]
    """

    NUMERIC_FIELDS = {
        "interest_score",
        "search_visibility_score",
        "result_count",
        "count",
        "frequency",
        "job_count",
    }

    INTEGER_FIELDS = {
        "result_count",
        "count",
        "frequency",
        "job_count",
    }

    @staticmethod
    def _clean_string(value: str) -> str | None:
        """
        Removes unnecessary whitespace from a string.
        """
        value = re.sub(r"\s+", " ", value).strip()

        if not value:
            return None

        return value

    @staticmethod
    def _clean_number(value: Any) -> int | float | None:
        """
        Converts values such as:
        '1,200,000' -> 1200000
        '85.4%' -> 85.4
        """
        if value is None:
            return None

        if isinstance(value, bool):
            return None

        if isinstance(value, (int, float)):
            return value

        if not isinstance(value, str):
            return None

        cleaned_value = value.strip()

        if not cleaned_value:
            return None

        cleaned_value = cleaned_value.replace(",", "")
        cleaned_value = cleaned_value.replace("%", "")

        try:
            number = float(cleaned_value)

            if number.is_integer():
                return int(number)

            return number

        except ValueError:
            return None

    def _clean_record(self, record: dict) -> dict | None:
        """
        Cleans one extracted record.
        """
        if not isinstance(record, dict):
            return None

        cleaned_record = {}

        for key, value in record.items():
            clean_key = str(key).strip()

            if not clean_key:
                continue

            if isinstance(value, str):
                value = self._clean_string(value)

            if clean_key in self.NUMERIC_FIELDS:
                value = self._clean_number(value)

            cleaned_record[clean_key] = value

        skill = cleaned_record.get("skill")

        if not isinstance(skill, str):
            return None

        skill = self._clean_string(skill)

        if skill is None:
            return None

        cleaned_record["skill"] = skill.lower()

        source = cleaned_record.get("source")

        if isinstance(source, str):
            cleaned_record["source"] = source.strip().lower()

        source_name = cleaned_record.get("source_name")

        if isinstance(source_name, str):
            cleaned_record["source_name"] = source_name.strip().lower()

        for field in self.INTEGER_FIELDS:
            value = cleaned_record.get(field)

            if isinstance(value, float):
                cleaned_record[field] = int(round(value))

        return cleaned_record

    @staticmethod
    def _remove_duplicates(records: list[dict]) -> list[dict]:
        """
        Removes completely identical records.
        """
        unique_records = []
        seen = set()

        for record in records:
            record_key = json.dumps(
                record,
                sort_keys=True,
                default=str,
            )

            if record_key in seen:
                continue

            seen.add(record_key)
            unique_records.append(record)

        return unique_records

    def transform(self, records: list[dict] | None) -> list[dict]:
        """
        Cleans a list of extracted records.
        """
        if not records:
            return []

        cleaned_records = []

        for record in records:
            cleaned_record = self._clean_record(record)

            if cleaned_record is not None:
                cleaned_records.append(cleaned_record)

        return self._remove_duplicates(cleaned_records)


if __name__ == "__main__":
    sample_data = [
        {
            "skill": "  Python  ",
            "interest_score": "85.4",
            "result_count": "1,200,000",
        },
        {
            "skill": "JavaScript",
            "interest_score": "72%",
            "result_count": 950000,
        },
        {
            "skill": "",
            "interest_score": 50,
        },
    ]

    cleaner = DataCleaner()
    cleaned_data = cleaner.transform(sample_data)

    for item in cleaned_data:
        print(item)