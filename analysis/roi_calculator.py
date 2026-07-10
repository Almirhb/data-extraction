from typing import Any


class ROICalculator:
    """
    Calculates the financial ROI for learning a technical skill.

    Expected fields:
        learning_cost
        learning_hours
        hourly_rate
        annual_salary_increase

    Formula:
        total_investment =
            learning_cost + (learning_hours * hourly_rate)

        ROI (%) =
            (annual_benefit - total_investment)
            / total_investment
            * 100
    """

    REQUIRED_NUMERIC_FIELDS = {
        "learning_cost",
        "learning_hours",
        "hourly_rate",
        "annual_salary_increase",
    }

    @staticmethod
    def _to_number(value: Any) -> float:
        """
        Converts a value to float.

        Invalid or negative values are converted to 0.
        """
        if value is None or isinstance(value, bool):
            return 0.0

        if isinstance(value, (int, float)):
            return max(float(value), 0.0)

        if isinstance(value, str):
            cleaned_value = (
                value.strip()
                .replace(",", "")
                .replace("$", "")
                .replace("€", "")
                .replace("%", "")
            )

            try:
                return max(float(cleaned_value), 0.0)
            except ValueError:
                return 0.0

        return 0.0

    def calculate_record(self, record: dict) -> dict:
        """
        Calculates ROI for one skill record.
        """
        result = record.copy()

        learning_cost = self._to_number(
            record.get("learning_cost")
        )
        learning_hours = self._to_number(
            record.get("learning_hours")
        )
        hourly_rate = self._to_number(
            record.get("hourly_rate")
        )
        annual_benefit = self._to_number(
            record.get("annual_salary_increase")
        )

        time_cost = learning_hours * hourly_rate
        total_investment = learning_cost + time_cost
        net_benefit = annual_benefit - total_investment

        if total_investment > 0:
            roi_percentage = (
                net_benefit / total_investment
            ) * 100
        else:
            roi_percentage = None

        if annual_benefit > 0:
            monthly_benefit = annual_benefit / 12
            payback_months = total_investment / monthly_benefit
        else:
            payback_months = None

        result.update({
            "learning_cost": round(learning_cost, 2),
            "learning_hours": round(learning_hours, 2),
            "hourly_rate": round(hourly_rate, 2),
            "time_cost": round(time_cost, 2),
            "total_investment": round(total_investment, 2),
            "annual_benefit": round(annual_benefit, 2),
            "net_benefit": round(net_benefit, 2),
            "roi_percentage": (
                round(roi_percentage, 2)
                if roi_percentage is not None
                else None
            ),
            "payback_months": (
                round(payback_months, 2)
                if payback_months is not None
                else None
            ),
        })

        return result

    def transform(self, records: list[dict] | None) -> list[dict]:
        """
        Calculates ROI for a list of skill records.
        """
        if not records:
            return []

        calculated_records = []

        for record in records:
            if not isinstance(record, dict):
                continue

            skill = record.get("skill")

            if not isinstance(skill, str) or not skill.strip():
                continue

            calculated_records.append(
                self.calculate_record(record)
            )

        return calculated_records


if __name__ == "__main__":
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
    results = calculator.transform(sample_data)

    for item in results:
        print(item)