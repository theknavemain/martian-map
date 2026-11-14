"""Layer 5 — Survival Guide. "If you landed here, you would need…"

Plain-English summary of a site's own data row. Not real advice for
astronauts. Scores 1–2 warn, 3 says mixed, 4–5 name a strength.
No field, no line.
"""

import streamlit as st


def guide_line(score, low, mid, high):
    """Scores 1–2 warn, 3 says mixed, 4–5 name a strength."""
    if score <= 2:
        return low
    if score == 3:
        return mid
    return high


def show_guide(sites):
    """Render Layer 5 on the page."""
    st.header("3. Survival Guide — if you landed here, you'd need…")
    st.write("Plain-English summary of that site's own data row. "
             "Not real advice for astronauts.")
    names = sites["name"].tolist()
    guide_name = st.selectbox("Pick a site", names, key="guide_site")
    g = sites[sites["name"] == guide_name].iloc[0]
    st.markdown(f"### {g['name']} — Survival Score {int(g['survival_score'])}/100")

    st.write("- 💧 **Resources:** " + guide_line(
        int(g["resource_score"]),
        f"Bring water or extract it — little easy water here. Its row says: {g['water_ice']}",
        f"Mixed resources — plan how you'd get water. Its row says: {g['water_ice']}",
        f"Resources are this site's strength. Its row says: {g['water_ice']}"))
    st.write("- 🏔️ **Terrain:** " + guide_line(
        int(g["terrain_score"]),
        f"Landing and driving need extra care. Its row says: {g['terrain']}",
        f"Mixed terrain — flat in places, rough in others. Its row says: {g['terrain']}",
        "Terrain helps landing and travel here."))
    st.write("- 🌡️ **Temperature / Radiation:** " + guide_line(
        int(g["temp_radiation_score"]),
        "Heating, insulation and radiation shelter are critical here. "
        f"Its row says: {g['temperature_notes']}",
        "Mixed temperatures — plan for cold spells and shelter. "
        f"Its row says: {g['temperature_notes']}",
        "Temperature and radiation are among this site's better factors — "
        "still plan for day-night swings and shelter."))
    st.write("- ⚠️ **Hazards:** " + guide_line(
        int(g["hazard_safety_score"]),
        f"Extra care and shelter needed. Its row says: {g['hazards']}",
        f"Mixed hazards — plan around them. Its row says: {g['hazards']}",
        "Fewer hazards than most sites here."))
    st.write(f"- 🎈 **Pressure:** this site sits at {int(g['elevation_m']):,} m "
             "elevation — lower ground means thicker air, easier landings and "
             "a little more shielding from radiation. " + guide_line(
        int(g["pressure_score"]),
        "High ground here — thin air, harder landings, less shielding.",
        "Middling pressure — neither the thickest nor the thinnest air.",
        "Low ground here — thicker air helps landings and shielding."))
    st.write("- 🌬️ **Air profile:** " + guide_line(
        int(g["air_score"]),
        "Dust and wind are a real problem here — plan to protect panels and suits.",
        "Mixed dust and wind — expect dusty spells.",
        "Dust and wind are manageable here."))
