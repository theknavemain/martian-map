# app_week2_compare_draft.py — Martian Map Week 2 compare view (DRAFT, not merged)
#
# Who this is for: Satyam (Person B, data & logic) and Pogo (Person A, map & UI).
# What it does, in one line: puts two sites side by side from the LIVE
# data/sites.csv (first 5 sites only) and says which Survival Score is higher.
#
# Why this draft exists: Week 2's spec lists merging rows 6-10 first, but that
# decision is still pending, and the compare view does NOT have to wait for it.
# This draft works on the 5 live sites today; once rows 6-10 are approved and
# merged into sites.csv, the same code automatically offers all 10 sites —
# no code change needed, because it reads whatever sites.csv holds.
#
# What it is NOT: it does not touch sites.csv, does not merge the draft rows,
# and does not replace Pogo's Map & UI work. It reuses the v0 detail-card
# fields only — no new Mars facts are added here.
#
# HONEST LIMIT — same as v0: this file has no map at all, only the compare
# columns. The Folium map, the Survival Guide panel and a real Mars basemap
# are separate Week 2 pieces, in the order in
# docs/WEEK2_COMPARE_AND_GUIDE_DRAFT.md.
#
# How to run it (after `pip install streamlit pandas`):
#   streamlit run app_week2_compare_draft.py
# Run it from this folder so it finds data/sites.csv next to it.

import streamlit as st
import pandas as pd
from pathlib import Path

# --- Load the data (Satyam's file, untouched by this app) -------------------
CSV_PATH = Path(__file__).parent / "data" / "sites.csv"
sites = pd.read_csv(CSV_PATH)

# --- Check every Survival Score against the agreed formula ------------------
# Formula (from docs/SURVIVAL_SCORE.md):
#   (water*0.30 + terrain*0.25 + temperature*0.20
#    + hazard_safety*0.15 + sunlight*0.10) * 20
sites["score_check"] = (
    sites["water_score"] * 0.30
    + sites["terrain_score"] * 0.25
    + sites["temperature_score"] * 0.20
    + sites["hazard_safety_score"] * 0.15
    + sites["sunlight_score"] * 0.10
) * 20
sites["score_check"] = sites["score_check"].round()
bad_scores = sites[sites["score_check"] != sites["survival_score"]]

# --- Page -------------------------------------------------------------------
st.title("Martian Map — Compare view (Week 2 draft)")
st.write(
    "Pick two sites and see, side by side, why one scores higher than the "
    "other. Works on the live sites.csv today (5 sites); it will offer "
    "10 sites automatically once rows 6-10 are merged."
)

if not bad_scores.empty:
    st.warning(
        "Score check: these rows do not match the Survival Score formula — "
        "fix sites.csv before using them: " + ", ".join(bad_scores["name"])
    )
else:
    st.success(f"Score check passed: all {len(sites)} Survival Scores match the formula.")

# --- Pick two different sites ------------------------------------------------
names = sites["name"].tolist()
site_a_name = st.selectbox("First site", names, key="site_a")
# Default second site: never the same as the first.
default_b = names[1] if site_a_name == names[0] else names[0]
site_b_name = st.selectbox("Second site", names, index=names.index(default_b), key="site_b")
if site_a_name == site_b_name:
    st.info("Pick two different sites to compare — a site against itself tells you nothing.")
    st.stop()

site_a = sites[sites["name"] == site_a_name].iloc[0]
site_b = sites[sites["name"] == site_b_name].iloc[0]


def show_card(site):
    """One site's card, reusing only fields already in sites.csv (v0 style)."""
    st.markdown(f"### {site['name']} — Survival Score {int(site['survival_score'])}/100")
    st.write(f"**Water:** {int(site['water_score'])}/5")
    st.write(f"**Terrain:** {int(site['terrain_score'])}/5")
    st.write(f"**Temperature:** {int(site['temperature_score'])}/5")
    st.write(f"**Hazard safety:** {int(site['hazard_safety_score'])}/5")
    st.write(f"**Sunlight:** {int(site['sunlight_score'])}/5")
    st.write(f"**Mission:** {site['mission']}")
    st.write(f"**Terrain:** {site['terrain']}")
    st.write(f"**Temperature:** {site['temperature_notes']}")
    st.write(f"**Water / ice:** {site['water_ice']}")
    st.write(f"**Hazards:** {site['hazards']}")
    st.write(site["description"])
    st.write(f"**Source:** {site['source_url']}")


col_a, col_b = st.columns(2)
with col_a:
    show_card(site_a)
with col_b:
    show_card(site_b)

# --- Verdict: higher score wins; a tie is a tie, no invented tie-breaker ---
st.subheader("Verdict")
score_a = int(site_a["survival_score"])
score_b = int(site_b["survival_score"])
if score_a > score_b:
    st.write(f"{site_a_name} ({score_a}) scores higher than {site_b_name} ({score_b}).")
elif score_b > score_a:
    st.write(f"{site_b_name} ({score_b}) scores higher than {site_a_name} ({score_a}).")
else:
    st.write(f"{site_a_name} and {site_b_name} are a tie at {score_a}.")
