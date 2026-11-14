# app_week2_basemap_draft.py — Martian Map Week 2 Mars basemap (DRAFT, not merged)
#
# Who this is for: Satyam (Person B, data & logic) and Pogo (Person A, map & UI).
# What it does, in one line: the same 5 live sites from data/sites.csv, but
# on a real Mars background instead of Folium's default Earth background,
# with a layer switcher so you can compare two Mars backgrounds.
#
# Why this draft exists: the v0 draft's own note says its background is a
# placeholder, not Mars imagery, and swapping in a real Mars basemap is the
# last step in the Week 2 spec
# (docs/WEEK2_COMPARE_AND_GUIDE_DRAFT.md: merge rows 6-10 -> compare view
# -> guide panel -> Mars basemap). The compare view draft (2026-10-31) and
# the guide panel draft (2026-11-01) are already delivered; this is the
# remaining piece. Like those drafts, it does NOT have to wait for the
# rows 6-10 decision: it reads whatever sites.csv holds, so it will offer
# 10 sites automatically once rows 6-10 are merged.
#
# The two backgrounds, both from the OpenPlanetaryMap basemaps wiki
# (https://github.com/openplanetary/opm/wiki/OPM-Basemaps, read 2026-11-01):
#   1. Viking MDIM2.1 Colorized Mosaic — real Mars surface imagery,
#      attribution NASA/Viking/USGS. TMS option required, so
#      folium.TileLayer(..., tms=True) is used for this layer.
#   2. OPM Mars Basemap v0.1, no labels — a cleaner vector-style Mars map,
#      attribution OpenPlanetaryMap. No TMS note on the wiki for this one.
# Use the layer control (top right of the map) to switch between them.
# The Viking layer is the default.
#
# What it is NOT: it does not touch sites.csv, does not merge the draft
# rows, does not replace Pogo's Map & UI work, and it does not add any new
# Mars facts — the pins, popups and scores all come from sites.csv alone.
#
# HONEST LIMIT — same as the v0, compare and guide drafts: a full
# `streamlit run` was not verified in the research environment, and the
# tile servers were not live-checked from there either, so your own run is
# the real proof. If a background loads blank, try the other layer first,
# then check your internet connection — do not assume the pins are wrong
# when only the background fails.
#
# How to run it (after `pip install streamlit folium pandas`):
#   streamlit run app_week2_basemap_draft.py
# Run it from this folder so it finds data/sites.csv next to it.

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
st.title("Martian Map — Week 2 Mars basemap draft")
st.write(
    "The same sites from sites.csv, now on a Mars background. "
    "Use the layer control on the map to switch backgrounds."
)

if not bad_scores.empty:
    st.warning(
        "Score check: these rows do not match the Survival Score formula — "
        "fix sites.csv before using them: "
        + ", ".join(bad_scores["name"])
    )
else:
    st.success(f"Score check passed: all {len(sites)} Survival Scores match the formula.")

# --- Map, with NO Earth background ------------------------------------------
# tiles=None means Folium adds no default layer; the Mars layers below
# are the only backgrounds.
mars_map = folium.Map(location=[0, 0], zoom_start=2, tiles=None)

# Layer 1 (default): Viking MDIM2.1 Colorized Mosaic — NASA/Viking/USGS.
# Wiki note: "TMS option required" -> tms=True.
folium.TileLayer(
    tiles="http://s3-eu-west-1.amazonaws.com/whereonmars.cartodb.net/viking_mdim21_global/{z}/{x}/{y}.png",
    attr="NASA/Viking/USGS (via OpenPlanetaryMap)",
    name="Mars — Viking imagery",
    tms=True,
    max_zoom=7,
).add_to(mars_map)

# Layer 2: OPM Mars Basemap v0.1, no labels — OpenPlanetaryMap.
folium.TileLayer(
    tiles="https://cartocdn-gusc.global.ssl.fastly.net/opmbuilder/api/v1/map/named/opm-mars-basemap-v0-1/0,1,2,3,4/{z}/{x}/{y}.png",
    attr="OpenPlanetaryMap",
    name="Mars — OPM basemap (no labels)",
    max_zoom=7,
).add_to(mars_map)

folium.LayerControl().add_to(mars_map)

for _, row in sites.iterrows():
    folium.Marker(
        location=[row["latitude"], row["longitude"]],
        popup=f"{row['name']} — Survival Score {int(row['survival_score'])}/100",
        tooltip=row["name"],
    ).add_to(mars_map)

components.html(mars_map._repr_html_(), height=500)

st.caption(
    "Backgrounds: Viking MDIM2.1 Colorized Mosaic (NASA/Viking/USGS) and "
    "OPM Mars Basemap v0.1 (OpenPlanetaryMap). Pins and scores are from "
    "sites.csv only."
)

# --- Ranking, same as v0, so the basemap change is the only difference -----
st.subheader("Ranking — best Survival Score first")
st.dataframe(
    sites.sort_values("survival_score", ascending=False)[
        ["name", "survival_score", "water_score", "terrain_score",
         "temperature_score", "hazard_safety_score", "sunlight_score"]
    ],
    hide_index=True,
)

# What is still NOT in this draft (deliberately, as separate drafts):
#   - the compare view: app_week2_compare_draft.py
#   - the Survival Guide panel: app_week2_guide_draft.py
# Merging all three into one app is Pogo's Map & UI step, not this draft.
