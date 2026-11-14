# Martian Map — Interplanetary Survival Guide

Where could humans survive on Mars? An interactive map of five real
landing-site candidates, ranked by a Survival Score built from their own
NASA/ESA data. The most famous site, Jezero Crater, is NOT the best place
to survive — this map shows why.

Built for the **NASA Space Apps Challenge 2026** (Nov 14–15). Team of two:
Satyam (data & logic — this repo) and Pogo (map & UI — main app).
This repo is Satyam's **backup app**, in case the main app hits trouble.

## What it does

- **Map** — real Mars backgrounds (Viking imagery + OpenPlanetaryMap), pins
  coloured by score, click a pin for its score
- **Ranking** — all 5 sites, best Survival Score first
- **Compare** — any two sites side by side, factor by factor, with a verdict
- **Survival Guide** — "if you landed here, you would need…" in plain English
- **Your priorities** — sliders re-weight the six factors and the ranking
  re-sorts live: survival has no single fixed score, it depends on the mission
- **Survival Kit** — a packing list built from each site's weak factors, with
  its single biggest threat called out
- **Plan Your Landing** — crew size, mission length and top priority in;
  a recommended site and a mission brief out

## The Survival Score (v2)

```
score = (resources×0.25 + temp/radiation×0.20 + terrain×0.20
         + hazards×0.15 + pressure×0.10 + air×0.10) × 20
```

Six factors, 1–5 each, out of 100. Current ranking: **Oxia Planum 78 =
Utopia Planitia 78** (tied top), Elysium Planitia 70, Gale Crater 68,
Jezero Crater 62. Full reasoning, sources and honest caveats:
[`docs/SURVIVAL_SCORE.md`](docs/SURVIVAL_SCORE.md).

## Project layout — one layer per file

```
martian-map/
├── app.py            entry point only (Layer 6: page shell)
├── score.py          Layer 1 — v2 formula + score check + custom weights
├── map_view.py       Layer 2 — Mars map + pins
├── ranking_view.py   Layer 3 — ranking table
├── compare_view.py   Layer 4 — compare two sites
├── guide_view.py     Layer 5 — Survival Guide panel
├── priorities_view.py  Layer 7 — priority sliders, live re-ranking
├── kit_view.py       Layer 8 — survival kit + biggest threat
├── mission_view.py   Layer 9 — plan your landing
├── requirements.txt
├── data/
│   ├── sites.csv                  5 live sites (the only data the app reads)
│   └── sites_rows6-10_DRAFT.csv  NOT merged — still scored on retired v1
├── docs/             formula, pitch lines, demo script, research sources
├── tests/
│   └── test_score.py Layer 1 test — run it before touching the UI
└── archive/          superseded single-file drafts (kept, not run)
```

Each layer only talks to the one below it. If the map breaks, the data and
scoring are already proven fine — debug one layer, not the whole app.

## Run it

Python 3.10+.

```bash
pip install -r requirements.txt
python3 tests/test_score.py   # Layer 1 check — all 5 scores must PASS
streamlit run app.py          # opens in your browser
```

## Deploy it (free)

1. Push this folder to a GitHub repo
2. Go to [share.streamlit.io](https://share.streamlit.io) → New app
3. Pick the repo, branch, and `app.py` — it installs `requirements.txt` itself

## Rules

- Every site fact needs a real source (NASA/JPL/USGS/ESA/peer-reviewed).
  Never invent Mars data.
- Never change a weight without updating `docs/SURVIVAL_SCORE.md` AND
  `score.py` together.
- The score check in the app must stay green before any demo.
