"""Layer 7 — Priorities. "What matters most to YOU?"

Sliders let the user re-weight the six v2 factors. The ranking re-sorts
live, which proves the point that survival has no single fixed score —
it depends on the mission. The stored v2 scores never change; this layer
only shows the same sites under the user's weights.

Slider defaults are the v2 weights scaled to 0–5:
resources 5, temp/radiation 4, terrain 4, hazards 3, pressure 2, air 2.
"""

import streamlit as st

from score import DEFAULT_WEIGHTS, weighted_score

FACTOR_LABELS = [
    ("Resources", "resource_score"),
    ("Temp / Radiation", "temp_radiation_score"),
    ("Terrain", "terrain_score"),
    ("Hazards", "hazard_safety_score"),
    ("Pressure", "pressure_score"),
    ("Air profile", "air_score"),
]


def slider_weights():
    """One slider per factor. Returns a weights dict, or None if all zero."""
    st.header("4. What matters most to YOU?")
    st.write(
        "Survival has no single fixed score — it depends on your mission. "
        "Drag the sliders and watch the ranking change. The stored v2 scores "
        "never change; this is the same data, seen through your priorities."
    )
    weights = {}
    cols = st.columns(3)
    for i, (label, key) in enumerate(FACTOR_LABELS):
        with cols[i % 3]:
            default = round(DEFAULT_WEIGHTS[key] * 20)
            weights[key] = st.slider(label, 0, 5, default, key=f"w_{key}")
    if sum(weights.values()) == 0:
        st.warning("All sliders are at 0 — at least one factor has to matter.")
        return None
    return weights


def show_priorities(sites):
    """Render Layer 7 on the page."""
    weights = slider_weights()
    if weights is None:
        return

    ranked = sites.copy()
    ranked["your_score"] = ranked.apply(lambda r: weighted_score(r, weights), axis=1)
    ranked["v2_rank"] = ranked["survival_score"].rank(ascending=False, method="min").astype(int)
    ranked = ranked.sort_values("your_score", ascending=False).reset_index(drop=True)
    ranked["your_rank"] = ranked.index + 1
    ranked["move"] = ranked.apply(
        lambda r: "—" if r["your_rank"] == r["v2_rank"]
        else f"↑ {r['v2_rank'] - r['your_rank']}" if r["your_rank"] < r["v2_rank"]
        else f"↓ {r['your_rank'] - r['v2_rank']}",
        axis=1,
    )
    st.subheader("Your ranking — same sites, your priorities")
    st.dataframe(
        ranked[["name", "your_score", "survival_score", "move"]].rename(
            columns={"survival_score": "v2_score"}
        ),
        hide_index=True,
        use_container_width=True,
    )
    top = ranked.iloc[0]
    st.success(
        f"Under your priorities, **{top['name']}** comes first at "
        f"{int(top['your_score'])}/100 (v2 score {int(top['survival_score'])})."
    )
