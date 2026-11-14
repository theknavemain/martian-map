# Week 2 draft — Compare view + Survival Guide panel (DRAFT, not v0)

Status: draft spec for Week 2 (31 Oct – 6 Nov 2026), after the Oct 30 v0.
It does not change `sites.csv` or `app_v0_draft.py`. Pogo (Map & UI) owns the
building; Satyam (Data & Logic) owns the wording below.

## 1. Compare view — two sites side by side

What the user does:
1. Pick Site A from a dropdown.
2. Pick Site B from a second dropdown (default: a different site, so the
   comparison is never a site against itself).
3. See them side by side, in two columns.

What each column shows — only fields already in `sites.csv`, no new data:
- Name and Survival Score out of 100 (big, at the top)
- The 5 factor scores: water, terrain, temperature, hazard safety, sunlight
- Mission, terrain, temperature notes, water/ice, hazards, description
- Source link

How to say who "wins": the higher Survival Score wins that comparison.
Say it in plain words, e.g. "Meridiani Planum (84) scores higher than
Jezero Crater (61) — mainly because it is flatter and sunnier."
If the scores tie, say "a tie" — do not invent a tie-breaker.

Beginner Streamlit shape (no new library):
```python
import streamlit as st
site_a = st.selectbox("First site", sites["name"].tolist())
site_b = st.selectbox("Second site", sites["name"].tolist())
col_a, col_b = st.columns(2)
# with col_a: show Site A's card; with col_b: show Site B's card
# Reuse the v0 detail-card code for each column, instead of writing it twice.
```

## 2. Survival Guide panel — "If you landed here, you would need…"

This panel sits under the detail card for the selected site. It does not
add new Mars facts — it turns the site's own row in `sites.csv` into
plain-English needs, using the 1–5 factor scores as the trigger:

- Water score 1–2: "You would need to bring water, or find a way to
  extract it — this site shows little easy water." (Use the site's
  `water_ice` field for the exact reason.)
- Water score 4–5: "Water is this site's strength — plan how to dig,
  melt and store it." (Again, quote the site's own `water_ice` field.)
- Temperature score 1–2: "Heating and insulation are critical — this is
  a very cold site." (Quote `temperature_notes`.)
- Hazard safety score 1–2: "Landing and driving here need extra care —
  shelter from the hazards in this site's `hazards` field."
- Sunlight score 1–2: "Solar power alone is weak here — plan for long
  dark periods and extra stored power."
- Scores of 3: say "mixed" and quote the field, not a strong warning.

Rule: every line in this panel must point back to a field in that site's
row. If a need is not in the row, do not write it — that is a data gap
for Satyam to research, not something to guess.

Example — Jezero Crater (61), from its existing row:
"If you landed here, you would need: strong protection and careful
driving around rocks and delta cliffs; a water plan, because its water
is in ancient lake clays, not an easy ice deposit; and heating for
large day–night temperature swings."

## 3. Order of work in Week 2

1. Merge the reviewed rows 6–10 into `sites.csv` first (v0 reads only
   that file) — compare view is only useful with 10 sites.
2. Build the compare view (section 1) — it reuses the v0 card.
3. Add the Survival Guide panel (section 2) — one short function that
   takes a site row and returns the bullet list.
4. Only then: the real Mars basemap (already listed as Week 2 polish
   in `app_v0_draft.py`).

## 4. Judge questions this answers (fact → so-what)

- "Why compare two sites instead of just ranking them?"
  Fact: a ranking hides why a site scored that way. So-what: side-by-side
  factor scores show the trade-off — e.g. best water is not always the
  best place to live.
- "Is your Survival Guide real advice for astronauts?"
  Fact: no — it is a plain-English summary of the site's own data row.
  So-what: it shows we understand what each score would mean in practice,
  without pretending to be a mission plan.

## Single next action (when Week 2 starts)

Pogo: add the two dropdowns and two columns from section 1, reusing the
v0 detail card. Satyam: check the Survival Guide wording for one site
(Jezero) against its `sites.csv` row before it is copied to the others.
