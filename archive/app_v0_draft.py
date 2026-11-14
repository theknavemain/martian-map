# app_v0_draft.py — Martian Map v0 (DRAFT starter, not the final app)
#
# Who this is for: Satyam (Person B, data & logic) and Pogo (Person A, map & UI).
# What it does, in one line: reads data/sites.csv and puts its sites on a
# clickable map, with a detail card and a Survival Score check.
#
# What it is NOT: the finished hackathon app. The compare view, the Survival
# Guide panel and a real Mars basemap are Week 2 work. Pogo still owns the
# map & UI — this draft exists so the v0 milestone (Fri 30 Oct: a working
# map + the first 5 sites) does not stall if Pogo is quiet this weekend.
#
# HONEST v0 LIMITATION — read this before showing it to anyone:
# Folium's default background is an Earth map. The pins are plotted from
# Mars latitudes/longitudes in sites.csv, so their positions relative to
# each other are right, but the picture underneath is NOT Mars. Swapping
# in a real Mars basemap is a Week 2 polish job, not a v0 blocker — do not
# present this background as Mars surface imagery.
#
# How to run it (after `pip install streamlit folium pandas`):
#   streamlit run app_v0_draft.py
# It reads data/sites.csv next to this file, so run it from this folder
# or keep the two files together when you copy them into the GitHub repo.

import streamlit as st
import pandas as pd
import folium
import streamlit.components.v1 as components
from pathlib import Path

# --- Load the data (Satyam's file, untouched by this app) -------------------
CSV_PATH = Path(__file__).parent / "data" / "sites.csv"
sites = pd.read_csv(CSV_PATH)

# --- Check every Survival Score against the agreed formula ------------------
# Formula (from docs/SURVIVAL_SCORE.md):
#   (water*0.30 + terrain*0.25 + temperature*0.20
#    + hazard_safety*0.15 + sunlight*0.10) * 20
# If a row's stored score disagrees with this, the app says so instead of
# silently showing a wrong number — that is Satyam's data-checking job.
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
st.title("Martian Map — v0")
st.write(
    "An interactive map of Mars that tells a future astronaut where they "
    "could survive, and why. v0: the first 5 sites from sites.csv."
)
st.caption(
    "v0 note: the map background below is a placeholder, not Mars imagery. "
    "The pins come from sites.csv — see the note at the top of this file."
)

if not bad_scores.empty:
    st.warning(
        "Score check: these rows do not match the Survival Score formula — "
        "fix sites.csv before using them: "
        + ", ".join(bad_scores["name"])
    )
else:
    st.success(f"Score check passed: all {len(sites)} Survival Scores match the formula.")

# --- Map --------------------------------------------------------------------
# Centre on Mars' equator (0, 0) and zoom out so all 5 sites are visible.
mars_map = folium.Map(location=[0, 0], zoom_start=2)
for _, row in sites.iterrows():
    folium.Marker(
        location=[row["latitude"], row["longitude"]],
        popup=f"{row['name']} — Survival Score {int(row['survival_score'])}/100",
        tooltip=row["name"],
    ).add_to(mars_map)

# No streamlit-folium needed: Folium's own HTML is embedded directly.
components.html(mars_map._repr_html_(), height=500)

# --- Detail card: pick a site, see why it scored that way -------------------
st.subheader("Site details")
chosen = st.selectbox("Choose a site", sites["name"].tolist())
site = sites[sites["name"] == chosen].iloc[0]

st.markdown(f"### {site['name']} — Survival Score {int(site['survival_score'])}/100")
st.write(f"**Mission:** {site['mission']}")
st.write(f"**Terrain:** {site['terrain']}")
st.write(f"**Temperature:** {site['temperature_notes']}")
st.write(f"**Water / ice:** {site['water_ice']}")
st.write(f"**Hazards:** {site['hazards']}")
st.write(site["description"])
st.write(f"**Source:** {site['source_url']}")

# --- Ranking table: best place to survive first ------------------------------
st.subheader("Ranking — best Survival Score first")
st.dataframe(
    sites.sort_values("survival_score", ascending=False)[
        ["name", "survival_score", "water_score", "terrain_score",
         "temperature_score", "hazard_safety_score", "sunlight_score"]
    ],
    hide_index=True,
)

# Next steps after v0 works (Week 2, not now):
#   1. Merge the reviewed rows 6-10 draft into sites.csv (it is a separate
#      draft file; this app reads only data/sites.csv until then).
#   2. Add the compare view (two sites side by side).
#   3. Add the Survival Guide panel ("If you landed here, you would need...").
#   4. Replace the placeholder background with a real Mars basemap.
