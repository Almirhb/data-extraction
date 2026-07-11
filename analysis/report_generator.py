from datetime import datetime

from storage.pipeline_db import get_all_skills_with_roi

REPORT_OUTPUT_PATH = "reports/skill_roi_report.md"


def generate_report(conn, output_path: str = REPORT_OUTPUT_PATH):
    """
    Builds a simple markdown report ranking skills by ROI score,
    from highest to lowest, and writes it to disk.
    """
    skills = get_all_skills_with_roi(conn)

    lines = [
        "# Skill ROI Report",
        f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "| Rank | Skill | ROI Score |",
        "|------|-------|-----------|",
    ]

    for rank, (skill_name, roi_score) in enumerate(skills, start=1):
        lines.append(f"| {rank} | {skill_name} | {roi_score} |")

    report_text = "\n".join(lines)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report_text)

    print(f"Report saved to {output_path} ({len(skills)} skills).")
    return report_text