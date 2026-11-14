"""Layer 4 — Compare. Two sites side by side, factor by factor, + verdict."""

import pandas as pd
import streamlit as st

FACTORS = [
    ("Resources", "resource_score"),
    ("Temp / Radiation", "temp_radiation_score"),
    ("Terrain", "terrain_score"),
    ("Hazards", "hazard_safety_score"),
    ("Pressure", "pressure_score"),
    ("Air profile", "air_score"),
]


def show_card(site):
    """One site's detail card, using only fields already in sites.csv."""
    st.markdown(f"### {site['name']}")
    st.write(site["description"])
    st.write(f"**Water:** {site['water_ice']}")
    st.write(f"**Source:** {site['source_url']}")


def show_compare(sites):
    """Render Layer 4 on the page."""
    st.header("2. Compare two sites")
    names = sites["name"].tolist()
    col_pick_a, col_pick_b = st.columns(2)
    with col_pick_a:
        name_a = st.selectbox("First site", names, index=0, key="site_a")
    with col_pick_b:
        default_b = names[1] if name_a == names[0] else names[0]
        name_b = st.selectbox("Second site", names,
                              index=names.index(default_b), key="site_b")

    if name_a == name_b:
        st.info("Pick two different sites — a site against itself tells you nothing.")
        return

    a = sites[sites["name"] == name_a].iloc[0]
    b = sites[sites["name"] == name_b].iloc[0]

    # Factor-by-factor table, so the verdict is visible, not just claimed.
    st.dataframe(
        pd.DataFrame({
            "Factor (1–5)": [label for label, _ in FACTORS] + ["SURVIVAL SCORE"],
            name_a: [int(a[col]) for _, col in FACTORS] + [int(a["survival_score"])],
            name_b: [int(b[col]) for _, col in FACTORS] + [int(b["survival_score"])],
        }),
        hide_index=True,
        use_container_width=True,
    )

    score_a, score_b = int(a["survival_score"]), int(b["survival_score"])
    if score_a > score_b:
        st.success(f"🏆 {name_a} ({score_a}) beats {name_b} ({score_b}).")
    elif score_b > score_a:
        st.success(f"🏆 {name_b} ({score_b}) beats {name_a} ({score_a}).")
    else:
        st.info(f"It's a tie — both score {score_a}.")

    col_a, col_b = st.columns(2)
    with col_a:
        show_card(a)
    with col_b:
        show_card(b)
