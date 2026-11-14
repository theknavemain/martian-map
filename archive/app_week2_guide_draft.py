# app_week2_guide_draft.py — Martian Map Week 2 Survival Guide panel (DRAFT, not merged)
#
# Who this is for: Satyam (Person B, data & logic) and Pogo (Person A, map & UI).
# What it does, in one line: pick one site from the LIVE data/sites.csv
# (first 5 sites only) and turn that site's own row into plain-English
# "If you landed here, you would need…" lines.
#
# Why this draft exists: the Week 2 spec
# (docs/WEEK2_COMPARE_AND_GUIDE_DRAFT.md, section 2) lists this panel as
# the step after the compare view, and the compare view draft was delivered
# on 2026-10-31. This panel does NOT have to wait for the rows 6-10
# decision either: like the compare draft, it reads whatever sites.csv
# holds, so it will offer 10 sites automatically once rows 6-10 are merged.
#
# What it is NOT: it does not touch sites.csv, does not merge the draft
# rows, does not replace Pogo's Map & UI work, and it is NOT real advice
# for astronauts — it is a plain-English summary of the site's own data
# row, for the pitch and judge questions. No new Mars facts are added here.
#
# Rule, from the spec: every line points back to a field in that site's
# row. Scores of 1-2 give a warning, 3 gives "mixed", 4-5 gives a strength
# — each quoting the row field behind it. If a need is not in the row,
# it is not written here; that is a data gap to research, not a guess.
#
# HONEST LIMIT — same as the v0 and compare drafts: a full `streamlit run`
# was not verified in the research environment, so the user's own run is
# the real proof. This draft is only the guide panel — no map, no compare
# columns, no Mars basemap yet.
#
# How to run it (after `pip install streamlit pandas`):
#   streamlit run app_week2_guide_draft.py
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


def guide_lines(site):
    """Return the Survival Guide lines for one sites.csv row.

    Each line quotes the row field it comes from. No field, no line.
    Works on a pandas row or a plain dict with the same keys.
    """
    def score(key):
        return int(site[key])

    lines = []
    # Water
    if score("water_score") <= 2:
        lines.append(
            "Bring water, or find a way to extract it — this site shows "
            f"little easy water. Its row says: {site['water_ice']}"
        )
    elif score("water_score") == 3:
        lines.append(
            "A mixed water picture — plan how you would get water here. "
            f"Its row says: {site['water_ice']}"
        )
    else:
        lines.append(
            "Water is this site's strength — plan how to dig, melt and "
            f"store it. Its row says: {site['water_ice']}"
        )
    # Terrain
    if score("terrain_score") <= 2:
        lines.append(
            "Landing and driving here need extra care. "
            f"Its row says: {site['terrain']}"
        )
    elif score("terrain_score") == 3:
        lines.append(
            "Mixed terrain — flat in places, rough in others. "
            f"Its row says: {site['terrain']}"
        )
    else:
        lines.append(
            "Terrain helps landing and travel here. "
            f"Its row says: {site['terrain']}"
        )
    # Temperature — quote the notes, never claim a temperature not in the row
    if score("temperature_score") <= 2:
        lines.append(
            "Heating and insulation are critical — this is a very cold site. "
            f"Its row says: {site['temperature_notes']}"
        )
    elif score("temperature_score") == 3:
        lines.append(
            "Mixed temperatures — plan for cold spells. "
            f"Its row says: {site['temperature_notes']}"
        )
    else:
        lines.append(
            "Temperature is one of this site's better factors — still plan "
            "for day-night swings. "
            f"Its row says: {site['temperature_notes']}"
        )
    # Hazard safety
    if score("hazard_safety_score") <= 2:
        lines.append(
            "Landing and driving need extra care, and shelter from hazards. "
            f"Its row says: {site['hazards']}"
        )
    elif score("hazard_safety_score") == 3:
        lines.append(
            "Mixed hazards — plan around them rather than ignoring them. "
            f"Its row says: {site['hazards']}"
        )
    else:
        lines.append(
            "Fewer hazards than most sites here. "
            f"Its row says: {site['hazards']}"
        )
    # Sunlight
    if score("sunlight_score") <= 2:
        lines.append(
            "Solar power alone is weak here — plan for long dark periods "
            "and extra stored power."
        )
    elif score("sunlight_score") == 3:
        lines.append(
            "Mixed sunlight — do not count on solar power alone."
        )
    else:
        lines.append(
            "Sunlight is a strength here — solar power is well supported."
        )
    return lines


# --- Page -------------------------------------------------------------------
st.title("Martian Map — Survival Guide panel (Week 2 draft)")
st.write(
    "Pick one site and see, in plain English, what its own data row would "
    "mean if you landed there. This is a summary of the row, not real "
    "advice for astronauts. Works on the live sites.csv today (5 sites); "
    "it will offer 10 sites automatically once rows 6-10 are merged."
)

if not bad_scores.empty:
    st.warning(
        "Score check: these rows do not match the Survival Score formula — "
        "fix sites.csv before using them: " + ", ".join(bad_scores["name"])
    )
else:
    st.success(f"Score check passed: all {len(sites)} Survival Scores match the formula.")

names = sites["name"].tolist()
site_name = st.selectbox("Pick a site", names)
site = sites[sites["name"] == site_name].iloc[0]

st.markdown(f"### {site['name']} — Survival Score {int(site['survival_score'])}/100")
st.write(f"**Water:** {int(site['water_score'])}/5")
st.write(f"**Terrain:** {int(site['terrain_score'])}/5")
st.write(f"**Temperature:** {int(site['temperature_score'])}/5")
st.write(f"**Hazard safety:** {int(site['hazard_safety_score'])}/5")
st.write(f"**Sunlight:** {int(site['sunlight_score'])}/5")

st.subheader("If you landed here, you would need…")
for line in guide_lines(site):
    st.write(f"- {line}")
