"""Layer 2 — Map. The interactive Mars map with site pins.

Reads only sites.csv (via the rows passed in). Knows nothing about the
formula or the other layers. Both tile layers were live-checked
(Nov 2 and Nov 9, 2026) — if the map loads blank, switch layers with the
button top-right of the map before assuming the server is dead.
"""

import folium
import streamlit as st
import streamlit.components.v1 as components


def build_map(sites):
    """Build the Folium map. Returns it — rendering happens in show_map()."""
    mars_map = folium.Map(location=[0, 0], zoom_start=2, tiles=None)
    folium.TileLayer(
        tiles="http://s3-eu-west-1.amazonaws.com/whereonmars.cartodb.net/"
              "viking_mdim21_global/{z}/{x}/{y}.png",
        attr="NASA/Viking/USGS (via OpenPlanetaryMap)",
        name="Mars — Viking imagery",
        tms=True,
        max_zoom=7,
    ).add_to(mars_map)
    folium.TileLayer(
        tiles="https://cartocdn-gusc.global.ssl.fastly.net/opmbuilder/api/v1/map/"
              "named/opm-mars-basemap-v0-1/0,1,2,3,4/{z}/{x}/{y}.png",
        attr="OpenPlanetaryMap",
        name="Mars — OPM basemap (no labels)",
        max_zoom=7,
    ).add_to(mars_map)
    folium.LayerControl().add_to(mars_map)

    for _, row in sites.iterrows():
        score = int(row["survival_score"])
        color = "green" if score >= 75 else "orange" if score >= 65 else "red"
        folium.Marker(
            location=[row["latitude"], row["longitude"]],
            popup=f"<b>{row['name']}</b><br>Survival Score: {score}/100<br>"
                  f"Mission: {row['mission']}",
            tooltip=f"{row['name']} — {score}/100",
            icon=folium.Icon(color=color, icon="info-sign"),
        ).add_to(mars_map)
    return mars_map


def show_map(sites):
    """Render Layer 2 on the page."""
    st.header("1. Map — real Mars, not Earth")
    st.write("Pins are the 5 sites. Use the layer button (top-right of the map) "
             "to switch Mars backgrounds. Click a pin for its score.")
    components.html(build_map(sites)._repr_html_(), height=500)
    st.caption(
        "Backgrounds: Viking MDIM2.1 Colorized Mosaic (NASA/Viking/USGS) and "
        "OPM Mars Basemap v0.1 (OpenPlanetaryMap). Pins and scores: sites.csv only."
    )
