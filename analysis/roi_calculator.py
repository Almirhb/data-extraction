from storage.pipeline_db import upsert_roi_score

# how much each source contributes to the final ROI score
# these should add up to 1.0, adjust based on how much you trust each source
SOURCE_WEIGHTS = {
    "remoteok": 0.4,       # direct job demand, weighted highest
    "github": 0.2,         # project/ecosystem popularity
    "stackoverflow": 0.2,  # community activity/questions
    "trends": 0.2,         # general public interest
}


def normalize(value, min_value, max_value):
    """
    Min-max normalization, scales any value to a 0-100 range so different
    sources (job counts, stars, search interest) become comparable.
    """
    if max_value == min_value:
        return 0

    return ((value - min_value) / (max_value - min_value)) * 100


def calculate_roi_scores(conn):
    """
    Reads all SkillMetrics rows, normalizes demand_count per source,
    combines them using SOURCE_WEIGHTS, and saves the result into
    ROIScores for each skill.
    """
    cur = conn.cursor()
    cur.execute("SELECT skill_id, source, demand_count FROM SkillMetrics")
    rows = cur.fetchall()

    # group raw values by source first, so we can normalize within each source
    values_by_source = {}
    for skill_id, source, demand_count in rows:
        values_by_source.setdefault(source, []).append(demand_count)

    # min/max per source, needed for normalize()
    source_ranges = {
        source: (min(values), max(values))
        for source, values in values_by_source.items()
    }

    # now group by skill so we can combine all sources for each skill
    metrics_by_skill = {}
    for skill_id, source, demand_count in rows:
        metrics_by_skill.setdefault(skill_id, {})[source] = demand_count

    for skill_id, source_values in metrics_by_skill.items():
        weighted_total = 0
        weight_used = 0

        for source, demand_count in source_values.items():
            if source not in SOURCE_WEIGHTS:
                continue

            min_value, max_value = source_ranges[source]
            normalized_value = normalize(demand_count, min_value, max_value)

            weight = SOURCE_WEIGHTS[source]
            weighted_total += normalized_value * weight
            weight_used += weight

        # if a skill is missing data from some sources, rescale by the
        # weight we actually had, so it's not unfairly penalized
        if weight_used > 0:
            roi_score = weighted_total / weight_used
        else:
            roi_score = 0

        upsert_roi_score(conn, skill_id, round(roi_score, 2))

    print(f"Calculated ROI scores for {len(metrics_by_skill)} skills.")