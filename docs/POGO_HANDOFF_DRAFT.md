# Pogo handoff — DRAFT, not sent

Status: prepared Mon 9 Nov 2026 (evening), updated Tue 10 Nov 2026 to the
v2 Survival Score (adopted Tue 10 Nov from the notebook list) for the
Wed 11 – Thu 12 Nov slot in the Week 3 plan. Corrected Tue 10 Nov 2026
after the restructure: the combined draft moved to `archive/` (kept, not
run), so the share now points at the live layered backup `app.py` instead.
Nothing here has been sent to Pogo, and nothing here changes `data/sites.csv`
or any app file. Needs the user's go-ahead before sending. Do not mention
a possible third team member — the team stays two for now.

## What to share

- `app.py` — one app: map + compare + Survival Guide (layered: `score.py`,
  `map_view.py`, `ranking_view.py`, `compare_view.py`, `guide_view.py`).
  This is the same combined app, restructured one layer per file on
  Tue 10 Nov. Do NOT share `archive/app_week2_combined_draft.py` — it is
  the superseded single-file version, kept not run.
- `data/sites.csv` — the frozen 5 live sites, v2 scores: Oxia 78 and
  Utopia 78 (tied at the top), Elysium 70, Gale 68, Jezero 62.
  Do NOT include `data/sites_rows6-10_DRAFT.csv` (still v1-scored).
- `docs/PITCH_WORKSHEET.md` — Oxia + Jezero pitch lines filled in (v2).
- `docs/DEMO_SCRIPT_60S_DRAFT.md` — the 60-second demo script (v2).

Verified Tue 10 Nov: the backup `app.py` compiles (`python3 -m py_compile`
OK) and all 5 v2 scores recompute exactly from `sites.csv` (test run
`python3 tests/test_score.py` — all 5 PASS: Jezero 62, Gale 68, Elysium 70,
Oxia 78, Utopia 78); its three sections match the demo script beats
exactly — 1. Map, 2. Compare two sites, 3. Survival Guide panel.

## How Pogo runs it

From the `martian-map` folder:

```
streamlit run app.py
```

## Three checks for Pogo (one clean run)

1. Map shows the real Mars background with 5 pins; ranking starts with
   Oxia 78 and Utopia 78 tied at the top.
2. Compare Oxia (78) vs Jezero (62) — verdict reads correctly.
3. Survival Guide on Utopia Planitia — resources strength (buried ice)
   shows, with the "mixed temperatures — plan for cold spells" line quoting
   its 47°N cold / less-sunlight note. (v2 change: sunlight is no longer a
   separate factor, so there is no standalone weak-sunlight warning.)

Fix only what breaks. No new features, no new sites.

## Draft message to Pogo (user to approve / edit first)

> Hi Pogo — sharing the combined app for Wed–Thu: map + compare + guide,
> on the frozen 5 sites (Oxia and Utopia tied at the top on 78, v2 formula).
> Run `streamlit run
> app.py` from the martian-map folder and try the
> three checks above. Pitch lines for Oxia and Jezero are in the worksheet,
> and the 60-second demo script is in the docs folder. Let me know if it
> runs clean on your machine, or what breaks.
>
> One more check for both of us before Saturday: are we both registered on
> spaceappschallenge.org and on the same team? I haven't confirmed that yet.

## Still unknown — ask the user, don't assume

- How to share it: is there a shared GitHub repo yet, or send the folder
  another way? (Pogo was to create the repo on 23 Oct; no repo link seen.)
- Registration status: still unconfirmed whether either teammate has
  registered and joined the same team (asked 3 Nov, no reply recorded).
  Registration stays open until the hackathon closes Sun 15 Nov; submission
  opens Sat 14 Nov 9:00 AM and closes Sun 15 Nov 11:59 PM local time.
- The user's own full run of the combined app is still unconfirmed.
- The 60-second demo script has not been confirmed read aloud / timed yet.
