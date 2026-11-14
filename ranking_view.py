"""Layer 3 — Ranking. The sorted table, best Survival Score first."""

import streamlit as st

FACTOR_COLUMNS = [
    "resource_score",
    "temp_radiation_score",
    "terrain_score",
    "hazard_safety_score",
    "pressure_score",
    "air_score",
]


def show_ranking(sites):
    """Render Layer 3 on the page."""
    st.subheader("Ranking — best Survival Score first")
    ranked = sites.sort_values("survival_score", ascending=False)
    st.dataframe(
        ranked[["name", "survival_score"] + FACTOR_COLUMNS],
        hide_index=True,
        use_container_width=True,
    )
    st.caption(
        "Top of the list is a tie at 78 — Oxia Planum and Utopia Planitia. "
        "Oxia wins on balance, Utopia wins on water alone (resource 5)."
    )
