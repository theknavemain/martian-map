"""Layer 9 — Plan Your Landing. The mission planner.

Three questions — crew size, mission length in sols, top priority — and
the app recommends one site and writes the mission brief: why this site,
the biggest threat, what to pack first, and what the mission length and
crew size change.

The rules are stated in the app, not hidden:
- your top priority's weight is doubled
- a long mission (300+ sols) raises the value of resources by half again —
  water recycling becomes non-optional
- a big crew (5+) raises the value of hazards/safety by half again —
  more people, more to protect
Weights are normalized, so the result is still a score out of 100.
"""

import streamlit as st

from kit_view import kit_for_site
from score import DEFAULT_WEIGHTS, weighted_score

FACTOR_LABELS = [
    ("Resources", "resource_score"),
    ("Temp / Radiation", "temp_radiation_score"),
    ("Terrain", "terrain_score"),
    ("Hazards", "hazard_safety_score"),
    ("Pressure", "pressure_score"),
    ("Air profile", "air_score"),
]
LABEL_TO_KEY = dict(FACTOR_LABELS)


def recommend(sites, crew, sols, priority_key):
    """Pure logic. Returns (ranked_df, top_row, brief_lines).

    ranked_df has a `mission_score` column, best first.
    """
    weights = dict(DEFAULT_WEIGHTS)
    weights[priority_key] *= 2
    if sols >= 300:
        weights["resource_score"] *= 1.5
    if crew >= 5:
        weights["hazard_safety_score"] *= 1.5

    ranked = sites.copy()
    ranked["mission_score"] = ranked.apply(lambda r: weighted_score(r, weights), axis=1)
    ranked = ranked.sort_values("mission_score", ascending=False).reset_index(drop=True)
    top = ranked.iloc[0]

    lines = []
    _, threat_line, items = kit_for_site(top)
    lines.append(f"**Why this site:** {top['name']} scores "
                 f"{int(top['mission_score'])}/100 under your mission profile "
                 f"(v2 score {int(top['survival_score'])}). "
                 f"Its strongest factors are "
                 + ", ".join(
                     label for label, key in FACTOR_LABELS
                     if int(top[key]) >= 4
                 ) + ".")
    lines.append(f"**Biggest threat:** {threat_line}")
    must_pack = [item for _, item, urgent in items if urgent]
    if must_pack:
        lines.append("**Pack first:** " + "; ".join(must_pack) + ".")
    else:
        lines.append("**Pack first:** " + items[0][1] + ".")
    if sols >= 300 and int(top["resource_score"]) <= 3:
        lines.append(
            f"**{sols} sols is a long stay:** water recycling is not optional "
            "here — the site's resources are only middling, so your recycling "
            "has to work every single sol."
        )
    if sols >= 300 and int(top["resource_score"]) >= 4:
        lines.append(
            f"**{sols} sols is a long stay:** the good news is this site's "
            "resources can carry it — water is one of its strengths."
        )
    if crew >= 5:
        lines.append(
            f"**A crew of {crew}:** a bigger crew needs a bigger habitat and "
            "more shielding — safety mattered more in this recommendation."
        )
    return ranked, top, lines


def show_mission(sites):
    """Render Layer 9 on the page."""
    st.header("6. Plan Your Landing")
    st.write(
        "Three questions, one recommendation. Your top priority counts "
        "double; a mission of 300+ sols makes resources matter half as much "
        "again; a crew of 5+ makes safety matter half as much again. "
        "The rules are right here — nothing is hidden."
    )
    col_crew, col_sols = st.columns(2)
    with col_crew:
        crew = st.slider("Crew size", 2, 6, 4, key="crew")
    with col_sols:
        sols = st.slider("Mission length (sols)", 30, 500, 180, step=30, key="sols")
    priority_label = st.selectbox(
        "Top priority",
        [label for label, _ in FACTOR_LABELS],
        key="priority",
    )
    priority_key = LABEL_TO_KEY[priority_label]

    ranked, top, lines = recommend(sites, crew, sols, priority_key)
    st.success(
        f"🚀 Recommended landing site: **{top['name']}** — "
        f"{int(top['mission_score'])}/100 for a crew of {crew} on a "
        f"{sols}-sol mission."
    )
    st.subheader("Your mission brief")
    for line in lines:
        st.write(f"- {line}")
    st.subheader("Top 3 sites for this mission")
    st.dataframe(
        ranked.head(3)[["name", "mission_score", "survival_score"]].rename(
            columns={"survival_score": "v2_score"}
        ),
        hide_index=True,
        use_container_width=True,
    )
