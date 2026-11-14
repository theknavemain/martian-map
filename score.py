"""Layer 1 — Scoring. The v2 Survival Score formula, nothing else.

Every score in the app comes from here. Change the weights ONLY together
with docs/SURVIVAL_SCORE.md — never one without the other.

Formula (v2):
    score = (resource*0.25 + temp_radiation*0.20 + terrain*0.20
             + hazards*0.15 + pressure*0.10 + air*0.10) * 20
"""

import pandas as pd

# The v2 weights. Sliders and the mission planner build their own weights,
# but the stored score always uses these.
DEFAULT_WEIGHTS = {
    "resource_score": 0.25,
    "temp_radiation_score": 0.20,
    "terrain_score": 0.20,
    "hazard_safety_score": 0.15,
    "pressure_score": 0.10,
    "air_score": 0.10,
}


def weighted_score(row, weights):
    """Score out of 100 for one row under ANY weights.

    Weights are normalized first, so sliders (0–5) and mission profiles
    (doubled priorities) work without the caller doing maths.
    With DEFAULT_WEIGHTS this is exactly survival_score().
    """
    total = sum(weights.values())
    if total == 0:
        raise ValueError("weights add up to 0 — at least one factor must matter")
    return round(sum(row[k] * w for k, w in weights.items()) / total * 20)


def survival_score(row):
    """v2 formula. Returns the score out of 100 for one sites.csv row."""
    return round(
        (
            row["resource_score"] * 0.25
            + row["temp_radiation_score"] * 0.20
            + row["terrain_score"] * 0.20
            + row["hazard_safety_score"] * 0.15
            + row["pressure_score"] * 0.10
            + row["air_score"] * 0.10
        )
        * 20
    )


def check_scores(sites):
    """Recompute every stored score. Returns the rows that DON'T match.

    An empty result means the data is trustworthy. A non-empty result
    means fix sites.csv before demoing — never hide it.
    """
    checked = sites.copy()
    checked["score_check"] = checked.apply(survival_score, axis=1)
    return checked[checked["score_check"] != checked["survival_score"]]


def load_sites(path):
    """Load the site table. Kept here so every layer reads the same file."""
    return pd.read_csv(path)
