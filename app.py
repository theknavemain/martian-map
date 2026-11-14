# app.py — Martian Map (BACKUP APP) — entry point only
#
# This file is Layer 6, the shell: page setup, data load, score check,
# then one call per layer. All the real work lives in the layer modules:
#   score.py         Layer 1 — v2 formula + score check
#   map_view.py      Layer 2 — Mars map + pins
#   ranking_view.py  Layer 3 — ranking table
#   compare_view.py  Layer 4 — compare two sites
#   guide_view.py    Layer 5 — Survival Guide panel
#   priorities_view.py  Layer 7 — "what matters most to you" sliders
#   kit_view.py      Layer 8 — survival kit + biggest threat
#   mission_view.py  Layer 9 — plan your landing (crew, sols, priority)
#
# Run from this folder:  streamlit run app.py

import streamlit as st
from pathlib import Path

from score import check_scores, load_sites
from map_view import show_map
from ranking_view import show_ranking
from compare_view import show_compare
from guide_view import show_guide
from priorities_view import show_priorities
from kit_view import show_kit
from mission_view import show_mission

CSV_PATH = Path(__file__).parent / "data" / "sites.csv"
sites = load_sites(CSV_PATH)

# --- Layer 6: page shell ----------------------------------------------------
st.set_page_config(page_title="Martian Map — Interplanetary Survival Guide",
                   layout="wide")
st.title("🪐 Martian Map — Interplanetary Survival Guide")
st.write(
    "Where could humans survive on Mars? Five real landing-site candidates, "
    "ranked by a Survival Score built from their own NASA/ESA data. "
    "The most famous site, Jezero Crater, is NOT the best place to survive — "
    "this map shows why."
)

bad = check_scores(sites)
if not bad.empty:
    st.error(
        "Score check FAILED for: " + ", ".join(bad["name"])
        + ". Fix sites.csv before demoing."
    )
else:
    st.success(f"✅ Score check passed — all {len(sites)} scores match the formula.")

# --- One call per layer, top to bottom --------------------------------------
show_map(sites)         # Layer 2
show_ranking(sites)     # Layer 3
show_compare(sites)     # Layer 4
show_guide(sites)       # Layer 5
show_priorities(sites)  # Layer 7 — your weights, live re-ranking
show_kit(sites)         # Layer 8 — what to pack
show_mission(sites)     # Layer 9 — plan your landing

# --- Footer -----------------------------------------------------------------
st.divider()
st.caption(
    "Formula (v2): score = (resources×0.25 + temp/radiation×0.20 + terrain×0.20 "
    "+ hazards×0.15 + pressure×0.10 + air×0.10) × 20. "
    "Every site fact comes from its source link in sites.csv "
    "(NASA/JPL, ESA, USGS). Built by Satyam as a backup to the main app."
)
