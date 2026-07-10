import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class ReportGenerator:
    """
    Generates summary reports from analyzed skill records.
    """

    @staticmethod
    def _valid_numbers(
        records: list[dict],
        field: str,
    ) -> list[float]:
        """
        Returns valid numeric values for a specific field.
        """
        values = []

        for record in records:
            value = record.get(field)

            if isinstance(value, bool):
                continue

            if isinstance(value, (int, float)):
                values.append(float(value))

        return values

    @staticmethod
    def _average(values: list[float]) -> float | None:
        """
        Calculates the average of numeric values.
        """
        if not values:
            return None

        return round(sum(values) / len(values), 2)

    @staticmethod
    def _top_record(
        records: list[dict],
        field: str,
    ) -> dict | None:
        """
        Returns the record with the highest value for a field.
        """
        valid_records = [
            record
            for record in records
            if isinstance(record.get(field), (int, float))
            and not isinstance(record.get(field), bool)
        ]

        if not valid_records:
            return None

        return max(
            valid_records,
            key=lambda record: record[field],
        )

    @staticmethod
    def _top_skill_summary(
        record: dict | None,
        field: str,
    ) -> dict | None:
        """
        Returns a compact representation of a top skill.
        """
        if record is None:
            return None

        return {
            "skill": record.get("skill"),
            field: record.get(field),
        }

    def generate(self, records: list[dict] | None) -> dict:
        """
        Generates the complete report dictionary.
        """
        if not records:
            records = []

        valid_records = [
            record
            for record in records
            if isinstance(record, dict)
        ]

        interest_scores = self._valid_numbers(
            valid_records,
            "interest_score",
        )

        roi_values = self._valid_numbers(
            valid_records,
            "roi_percentage",
        )

        total_investments = self._valid_numbers(
            valid_records,
            "total_investment",
        )

        annual_benefits = self._valid_numbers(
            valid_records,
            "annual_benefit",
        )

        top_interest_record = self._top_record(
            valid_records,
            "interest_score",
        )

        top_roi_record = self._top_record(
            valid_records,
            "roi_percentage",
        )

        sorted_records = sorted(
            valid_records,
            key=lambda record: (
                record.get("roi_percentage") is not None,
                record.get("roi_percentage") or 0,
            ),
            reverse=True,
        )

        return {
            "generated_at": datetime.now(
                timezone.utc
            ).isoformat(),
            "summary": {
                "total_skills": len(valid_records),
                "skills_with_roi": len(roi_values),
                "average_interest_score": self._average(
                    interest_scores
                ),
                "average_roi_percentage": self._average(
                    roi_values
                ),
                "total_investment": round(
                    sum(total_investments),
                    2,
                ),
                "total_annual_benefit": round(
                    sum(annual_benefits),
                    2,
                ),
                "top_skill_by_interest":
                    self._top_skill_summary(
                        top_interest_record,
                        "interest_score",
                    ),
                "top_skill_by_roi":
                    self._top_skill_summary(
                        top_roi_record,
                        "roi_percentage",
                    ),
            },
            "skills": sorted_records,
        }

    @staticmethod
    def save_json(
        report: dict,
        output_path: str | Path,
    ) -> Path:
        """
        Saves the report as JSON.
        """
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                report,
                file,
                indent=4,
                ensure_ascii=False,
            )

        return path

    @staticmethod
    def save_csv(
        records: list[dict],
        output_path: str | Path,
    ) -> Path:
        """
        Saves skill records as CSV.
        """
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        if not records:
            path.write_text("", encoding="utf-8")
            return path

        fieldnames = []

        for record in records:
            for key in record.keys():
                if key not in fieldnames:
                    fieldnames.append(key)

        with path.open(
            "w",
            newline="",
            encoding="utf-8",
        ) as file:
            writer = csv.DictWriter(
                file,
                fieldnames=fieldnames,
            )

            writer.writeheader()
            writer.writerows(records)

        return path

    @staticmethod
    def save_markdown(
        report: dict,
        output_path: str | Path,
    ) -> Path:
        """
        Saves a readable Markdown report.
        """
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        summary = report.get("summary", {})
        skills = report.get("skills", [])

        lines = [
            "# Skill Analysis Report",
            "",
            f"Generated at: {report.get('generated_at')}",
            "",
            "## Summary",
            "",
            f"- Total skills: {summary.get('total_skills', 0)}",
            (
                "- Average interest score: "
                f"{summary.get('average_interest_score')}"
            ),
            (
                "- Average ROI: "
                f"{summary.get('average_roi_percentage')}%"
            ),
            (
                "- Total investment: "
                f"{summary.get('total_investment')}"
            ),
            (
                "- Total annual benefit: "
                f"{summary.get('total_annual_benefit')}"
            ),
            "",
            "## Skills",
            "",
            "| Skill | Interest | Investment | "
            "Annual benefit | ROI | Payback |",
            "|---|---:|---:|---:|---:|---:|",
        ]

        for record in skills:
            lines.append(
                "| "
                f"{record.get('skill', '')} | "
                f"{record.get('interest_score', '')} | "
                f"{record.get('total_investment', '')} | "
                f"{record.get('annual_benefit', '')} | "
                f"{record.get('roi_percentage', '')}% | "
                f"{record.get('payback_months', '')} months |"
            )

        path.write_text(
            "\n".join(lines),
            encoding="utf-8",
        )

        return path


if __name__ == "__main__":
    from analysis.roi_calculator import ROICalculator

    sample_data = [
        {
            "skill": "python",
            "interest_score": 92,
            "learning_cost": 1000,
            "learning_hours": 120,
            "hourly_rate": 15,
            "annual_salary_increase": 6000,
        },
        {
            "skill": "javascript",
            "interest_score": 85,
            "learning_cost": 800,
            "learning_hours": 100,
            "hourly_rate": 15,
            "annual_salary_increase": 4500,
        },
        {
            "skill": "aws",
            "interest_score": 88,
            "learning_cost": 1500,
            "learning_hours": 150,
            "hourly_rate": 15,
            "annual_salary_increase": 8000,
        },
    ]

    calculator = ROICalculator()
    analyzed_records = calculator.transform(sample_data)

    generator = ReportGenerator()
    report = generator.generate(analyzed_records)

    json_path = generator.save_json(
        report,
        "data/reports/skill_analysis_report.json",
    )

    csv_path = generator.save_csv(
        analyzed_records,
        "data/reports/skill_analysis_report.csv",
    )

    markdown_path = generator.save_markdown(
        report,
        "data/reports/skill_analysis_report.md",
    )

    print(f"JSON report created: {json_path}")
    print(f"CSV report created: {csv_path}")
    print(f"Markdown report created: {markdown_path}")