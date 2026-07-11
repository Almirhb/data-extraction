from datetime import datetime

import matplotlib.pyplot as plt

from storage.pipeline_db import get_all_skills_with_roi

REPORT_OUTPUT_PATH = "reports/skill_roi_report.md"
CHART_OUTPUT_PATH = "reports/skill_roi_chart.png"
TOP_N = 15  # only show the top N skills on the chart, otherwise it gets unreadable


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


def generate_chart(conn, output_path: str = CHART_OUTPUT_PATH, top_n: int = TOP_N):
    """
    Builds a horizontal bar chart of the top N skills by ROI score
    and saves it as a PNG. Much easier to skim than the markdown table.
    """
    skills = get_all_skills_with_roi(conn)[:top_n]

    if not skills:
        print("No skills to chart yet, skipping.")
        return

    names = [s[0] for s in skills]
    scores = [s[1] for s in skills]

    # reverse so the highest score ends up at the top of the chart
    names.reverse()
    scores.reverse()

    plt.figure(figsize=(10, 8))
    plt.barh(names, scores, color="#4C72B0")
    plt.xlabel("ROI Score")
    plt.title(f"Top {top_n} Skills by ROI Score")
    plt.tight_layout()

    plt.savefig(output_path)
    plt.close()

    print(f"Chart saved to {output_path}")