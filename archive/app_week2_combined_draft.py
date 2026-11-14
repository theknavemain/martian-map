# app_week2_combined_draft.py — Martian Map Week 2, all pieces in one app (DRAFT)
#
# Who this is for: Satyam (Person B, data & logic) and Pogo (Person A, map & UI).
# What it does, in one line: the three separate Week 2 drafts, together —
# the Mars basemap with pins, the compare view, and the Survival Guide panel —
# in a single app, reading the same live data/sites.csv.
#
# Why this draft exists: Week 2 (Nov 2-8) delivered three separate scripts —
#   app_week2_compare_draft.py (Oct 31),
#   app_week2_guide_draft.py (Nov 1),
#   app_week2_basemap_draft.py (Nov 1, tiles live-checked Nov 2).
# Running three apps to demo one project is awkward, and a judge demo needs
# one app. This file only rearranges those three drafts into sections;
# it adds no new Mars facts and no new scoring. Every pin, popup, score,
# compare card and guide line still comes from sites.csv alone.
#
# What it is NOT: it does not touch sites.csv, does not merge the draft
# rows 6-10, does not replace Pogo's Map & UI work, and it is NOT real
# advice for astronauts — the guide panel is a plain-English summary of a
# site's own data row. It will offer 10 sites automatically once rows 6-10
# are merged, because it reads whatever sites.csv holds.
#
# HONEST LIMIT: a full `streamlit run` on the user's own machine is still
# the final proof. If a map background loads blank at a particular zoom,
# switch layers with the layer control first — the tile servers were
# live-checked on Nov 2, so a dead tile server is no longer a likely cause.
#
# How to run it (after `pip install streamlit folium pandas`):
#   streamlit run app_week2_combined_draft.py
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
# Formula (v2, from docs/SURVIVAL_SCORE.md):
#   (resource*0.25 + temp_radiation*0.20 + terrain*0.20
#    + hazards*0.15 + pressure*0.10 + air*0.10) * 20
sites["score_check"] = (
    sites["resource_score"] * 0.25
    + sites["temp_radiation_score"] * 0.20
    + sites["terrain_score"] * 0.20
    + sites["hazard_safety_score"] * 0.15
    + sites["pressure_score"] * 0.10
    + sites["air_score"] * 0.10
) * 20
sites["score_check"] = sites["score_check"].round()
bad_scores = sites[sites["score_check"] != sites["survival_score"]]

# --- Shared helpers, copied from the three Week 2 drafts --------------------


def show_card(site):
    """One site's card, reusing only fields already in sites.csv (v0 style)."""
    st.markdown(f"### {site['name']} — Survival Score {int(site['survival_score'])}/100")
    st.write(f"**Resources:** {int(site['resource_score'])}/5")
    st.write(f"**Temp / Radiation:** {int(site['temp_radiation_score'])}/5")
    st.write(f"**Terrain:** {int(site['terrain_score'])}/5")
    st.write(f"**Hazards:** {int(site['hazard_safety_score'])}/5")
    st.write(f"**Pressure:** {int(site['pressure_score'])}/5 "
             f"(elevation {int(site['elevation_m']):,} m)")
    st.write(f"**Air profile:** {int(site['air_score'])}/5")
    st.write(f"**Mission:** {site['mission']}")
    st.write(f"**Terrain:** {site['terrain']}")
    st.write(f"**Temperature:** {site['temperature_notes']}")
    st.write(f"**Water / ice:** {site['water_ice']}")
    st.write(f"**Hazards:** {site['hazards']}")
    st.write(site["description"])
    st.write(f"**Source:** {site['source_url']}")


def guide_lines(site):
    """Survival Guide lines for one sites.csv row (from the guide draft).

    Each line quotes the row field it comes from. Scores 1-2 warn,
    3 says mixed, 4-5 name a strength. No field, no line.
    """
    def score(key):
        return int(site[key])

    lines = []
    if score("resource_score") <= 2:
        lines.append(
            "Bring water, or find a way to extract it — this site shows "
            f"little easy water. Its row says: {site['water_ice']}"
        )
    elif score("resource_score") == 3:
        lines.append(
            "A mixed resources picture — plan how you would get water here. "
            f"Its row says: {site['water_ice']}"
        )
    else:
        lines.append(
            "Resources are this site's strength — plan how to dig, melt and "
            f"store it. Its row says: {site['water_ice']}"
        )
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
    if score("temp_radiation_score") <= 2:
        lines.append(
            "Heating, insulation and radiation shelter are critical — this is "
            "a very cold site. "
            f"Its row says: {site['temperature_notes']}"
        )
    elif score("temp_radiation_score") == 3:
        lines.append(
            "Mixed temperatures — plan for cold spells and shelter. "
            f"Its row says: {site['temperature_notes']}"
        )
    else:
        lines.append(
            "Temperature and radiation are among this site's better factors — "
            "still plan for day-night swings and shelter. "
            f"Its row says: {site['temperature_notes']}"
        )
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
    if score("pressure_score") <= 2:
        lines.append(
            "High ground here — thin air, harder landings, less shielding "
            f"from radiation (elevation {int(site['elevation_m']):,} m)."
        )
    elif score("pressure_score") == 3:
        lines.append(
            "Middling pressure — neither the thickest nor the thinnest air "
            f"(elevation {int(site['elevation_m']):,} m)."
        )
    else:
        lines.append(
            "Low ground here — thicker air helps landings and shielding "
            f"(elevation {int(site['elevation_m']):,} m)."
        )
    if score("air_score") <= 2:
        lines.append(
            "Dust and wind are a real problem here — plan to protect panels "
            "and suits."
        )
    elif score("air_score") == 3:
        lines.append("Mixed dust and wind — expect dusty spells.")
    else:
        lines.append("Dust and wind are manageable here.")
    return lines


# --- Page -------------------------------------------------------------------
st.title("Martian Map — Week 2 combined draft")
st.write(
    "Map, compare view and Survival Guide panel in one app, all reading "
    "the live sites.csv. Works on the 5 live sites today; it will offer "
    "10 sites automatically once rows 6-10 are merged."
)

if not bad_scores.empty:
    st.warning(
        "Score check: these rows do not match the Survival Score formula — "
        "fix sites.csv before using them: " + ", ".join(bad_scores["name"])
    )
else:
    st.success(f"Score check passed: all {len(sites)} Survival Scores match the formula.")

# --- Section 1: Mars map (from the basemap draft) ---------------------------
st.header("1. Map — real Mars background")
st.write("Use the layer control on the map to switch backgrounds.")
mars_map = folium.Map(location=[0, 0], zoom_start=2, tiles=None)
folium.TileLayer(
    tiles="http://s3-eu-west-1.amazonaws.com/whereonmars.cartodb.net/viking_mdim21_global/{z}/{x}/{y}.png",
    attr="NASA/Viking/USGS (via OpenPlanetaryMap)",
    name="Mars — Viking imagery",
    tms=True,
    max_zoom=7,
).add_to(mars_map)
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

st.subheader("Ranking — best Survival Score first")
st.dataframe(
    sites.sort_values("survival_score", ascending=False)[
        ["name", "survival_score", "resource_score", "temp_radiation_score",
         "terrain_score", "hazard_safety_score", "pressure_score", "air_score"]
    ],
    hide_index=True,
)

# --- Section 2: Compare view (from the compare draft) -----------------------
st.header("2. Compare two sites")
names = sites["name"].tolist()
site_a_name = st.selectbox("First site", names, key="site_a")
default_b = names[1] if site_a_name == names[0] else names[0]
site_b_name = st.selectbox("Second site", names, index=names.index(default_b), key="site_b")
if site_a_name == site_b_name:
    st.info("Pick two different sites to compare — a site against itself tells you nothing.")
else:
    site_a = sites[sites["name"] == site_a_name].iloc[0]
    site_b = sites[sites["name"] == site_b_name].iloc[0]
    col_a, col_b = st.columns(2)
    with col_a:
        show_card(site_a)
    with col_b:
        show_card(site_b)
    st.subheader("Verdict")
    score_a = int(site_a["survival_score"])
    score_b = int(site_b["survival_score"])
    if score_a > score_b:
        st.write(f"{site_a_name} ({score_a}) scores higher than {site_b_name} ({score_b}).")
    elif score_b > score_a:
        st.write(f"{site_b_name} ({score_b}) scores higher than {site_a_name} ({score_a}).")
    else:
        st.write(f"{site_a_name} and {site_b_name} are a tie at {score_a}.")

# --- Section 3: Survival Guide panel (from the guide draft) -----------------
st.header("3. Survival Guide panel")
st.write(
    "Pick one site and see, in plain English, what its own data row would "
    "mean if you landed there. This is a summary of the row, not real "
    "advice for astronauts."
)
guide_name = st.selectbox("Pick a site", names, key="guide_site")
guide_site = sites[sites["name"] == guide_name].iloc[0]
st.markdown(f"### {guide_site['name']} — Survival Score {int(guide_site['survival_score'])}/100")
st.subheader("If you landed here, you would need…")
for line in guide_lines(guide_site):
    st.write(f"- {line}")
