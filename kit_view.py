"""Layer 8 — Survival Kit. "What to pack" for each site.

The kit is built from the site's OWN weak factors — a factor of 1–2 is a
critical item, 3 is a standard item, 4–5 needs only basic gear. Nothing
here is invented: every item answers a factor the site actually scores
on, and the threat line names the site's single lowest factor.

Pure logic (kit_for_site) is kept separate from rendering (show_kit)
so it can be tested without Streamlit — and the mission planner reuses it.
"""

import streamlit as st

# Tie-break order for "biggest threat": the most lethal factor wins ties.
THREAT_ORDER = [
    "temp_radiation_score",
    "air_score",
    "hazard_safety_score",
    "terrain_score",
    "pressure_score",
    "resource_score",
]

FACTOR_LABELS = {
    "resource_score": "Resources",
    "temp_radiation_score": "Temp / Radiation",
    "terrain_score": "Terrain",
    "hazard_safety_score": "Hazards",
    "pressure_score": "Pressure",
    "air_score": "Air profile",
}

# Gear per factor, by score band. 1–2 = critical, 3 = standard, 4–5 = basic.
KIT = {
    "resource_score": {
        "low": "Water extraction rig + recycling unit — bring water, do not count on finding it",
        "mid": "Water recycling unit + prospecting drill",
        "high": "Standard water storage + ice drill",
    },
    "temp_radiation_score": {
        "low": "Heated habitat + radiation-shielded shelter (bury it or shield it)",
        "mid": "Insulated habitat + storm shelter",
        "high": "Standard insulation + shelter plan",
    },
    "terrain_score": {
        "low": "Precision landing system + rover built for rough ground",
        "mid": "Careful landing-site survey + rugged rover",
        "high": "Standard lander + rover",
    },
    "hazard_safety_score": {
        "low": "Hazard shielding + reinforced habitat",
        "mid": "Hazard survey before landing + shielding",
        "high": "Standard shielding",
    },
    "pressure_score": {
        "low": "Suits and lander rated for very thin air — slowing down is harder here",
        "mid": "Standard entry, descent and landing gear",
        "high": "Standard landing gear — thicker air helps you slow down",
    },
    "air_score": {
        "low": "Dust-proof seals, panel cleaners + spare filters",
        "mid": "Panel cleaning kit + dust filters",
        "high": "Standard dust protection",
    },
}

THREAT_LINES = {
    "resource_score": "Water is your biggest problem here — sort out how to get it before anything else.",
    "temp_radiation_score": "Cold and radiation are your biggest threat here.",
    "terrain_score": "Landing safely is your biggest threat here.",
    "hazard_safety_score": "Hazards are your biggest threat here.",
    "pressure_score": "Thin air is your biggest threat here — landings are harder and shielding is weaker.",
    "air_score": "Dust and wind are your biggest threat here.",
}


def _band(score):
    return "low" if score <= 2 else "mid" if score == 3 else "high"


def kit_for_site(site):
    """Pure logic. Returns (threat_factor_key, threat_line, [(label, item, urgent)]).

    Items are sorted most urgent first. `urgent` is True for the critical
    (1–2) items — the things that must be packed first.
    """
    scores = {k: int(site[k]) for k in FACTOR_LABELS}
    lowest = min(scores.values())
    threat_key = next(k for k in THREAT_ORDER if scores[k] == lowest)
    threat_line = THREAT_LINES[threat_key]
    items = []
    for key, label in FACTOR_LABELS.items():
        band = _band(scores[key])
        items.append((label, KIT[key][band], band == "low"))
    items.sort(key=lambda item: (not item[2], item[0]))
    return threat_key, threat_line, items


def show_kit(sites):
    """Render Layer 8 on the page."""
    st.header("5. Survival Kit — what to pack")
    st.write(
        "Every item below answers a weakness in that site's own data. "
        "Tick off what you would pack — the urgent items are the ones that "
        "decide whether the crew comes home."
    )
    names = sites["name"].tolist()
    kit_name = st.selectbox("Pack for this site", names, key="kit_site")
    site = sites[sites["name"] == kit_name].iloc[0]
    _, threat_line, items = kit_for_site(site)
    st.error(f"☠ Biggest threat at {site['name']}: {threat_line}")
    st.subheader(f"Packing list — {site['name']} (score {int(site['survival_score'])}/100)")
    for label, item, urgent in items:
        mark = "🔴 MUST PACK" if urgent else "✓"
        st.checkbox(f"{mark} — **{label}:** {item}", key=f"kit_{kit_name}_{label}")
