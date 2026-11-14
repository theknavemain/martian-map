# Survival Score v2 — APPLIED Tue 10 Nov 2026 (now live)

Status: adopted by the user on 10 Nov 2026. `SURVIVAL_SCORE.md`, `sites.csv`,
`app.py`, `app_week2_combined_draft.py`, the pitch worksheet and the demo
script have all been updated to v2. This file is kept as the working record
of the change.

## What changed vs v1

v1 (live): water 30% + terrain 25% + temperature 20% + hazard safety 15%
+ sunlight 10%.

v2 (this draft): 6 factors, from the notebook list.

| Factor | Question it answers | Weight | v1 equivalent |
|---|---|---|---|
| Resource Availability | Can we get water and useful minerals here — ice, or water-rich clays/minerals? | 25% | replaces Water (30%) |
| Temperature / Radiation | Warm enough, and shielded enough from cosmic radiation? | 20% | Temperature (20%), now with radiation |
| Terrain | Flat and safe enough to land and build on? | 20% | Terrain (25%) |
| Hazards | How few dangers (rocks, cliffs, dust traps)? 5 = very safe | 15% | Hazard safety (15%) |
| Pressure | Atmospheric pressure from elevation — lower ground = thicker air = easier landing + more shielding | 10% | NEW |
| Air Profile | Dust and wind — dust storms, dust build-up on panels, wind-blown grit | 10% | NEW |

Sunlight is dropped on purpose: it is mostly driven by latitude, which
Temperature already captures. Keeping all three (temperature + sunlight +
radiation) would count latitude three times. Solar power still matters —
a judge may ask where it went, and this is the answer.

## How the two new factors are scored (1–5, same scale)

### Pressure — from MOLA elevation (lower = better)
- 5: below −4,000 m
- 4: −3,000 to −4,000 m
- 3: −2,000 to −3,000 m
- 2: −1,000 to −2,000 m
- 1: above −1,000 m

Site elevations (landing-site records): Gale −4,501 m; Utopia (Viking 2)
−4,495 m; Jezero −2,640 m; Elysium (InSight) −2,613 m; Oxia ~−2,000 m.
Pressure scores: Jezero 3, Gale 5, Elysium 3, Oxia 3, Utopia 5.

### Temperature / Radiation — 70% temperature, 30% radiation shielding
Radiation uses the same elevation bands as Pressure, because the lowest
ground has the most air above it to block cosmic rays (JPL MARIE map:
lowest radiation where elevation is lowest; Mars' thin air cuts the dose
by roughly 30–50%). Score = round(0.7 × temperature + 0.3 × radiation).

- Jezero: temp 4, radiation 3 → 4
- Gale: temp 4, radiation 5 → 4
- Elysium: temp 5, radiation 3 → 4
- Oxia: temp 4, radiation 3 → 4
- Utopia: temp 2, radiation 5 → 3

### Air Profile — dust and wind (weakest data — see caveats)
- Jezero 4 (dust, moderate), Gale 3 (edge of a high-dust-cover region;
  dust devils), Elysium 3 (dust build-up ended InSight), Oxia 4
  (wind ripples, moderate dust), Utopia 3 (northern-plains dust).

## The formula
```
survival_score = (resource*0.25 + temp_radiation*0.20 + terrain*0.20
                  + hazards*0.15 + pressure*0.10 + air*0.10) * 20
```

## New scores (v2 vs v1)

| Site | Resource | Temp/Rad | Terrain | Hazards | Pressure | Air | v2 | v1 |
|---|---|---|---|---|---|---|---|---|
| Oxia Planum | 4 | 4 | 4 | 4 | 3 | 4 | **78** | 80 |
| Utopia Planitia | 5 | 3 | 4 | 3 | 5 | 3 | **78** | 71 |
| Elysium Planitia | 2 | 4 | 5 | 4 | 3 | 3 | **70** | 79 |
| Gale Crater | 3 | 4 | 3 | 3 | 5 | 3 | **68** | 68 |
| Jezero Crater | 3 | 4 | 2 | 3 | 3 | 4 | **62** | 61 |

Ranking: Oxia 78 = Utopia 78 (tie), Elysium 70, Gale 68, Jezero 62.

Worked example — Oxia Planum (78):
(4×0.25 + 4×0.20 + 4×0.20 + 4×0.15 + 3×0.10 + 4×0.10) × 20
= 3.90 × 20 = **78**

## Honest caveats (tell the judges these, don't hide them)

1. **Elevation is now counted twice.** Low ground wins Pressure (10%) AND
   part of Temperature/Radiation (30% of 20%). That is most of why Utopia
   jumps 71 → 78 and ties Oxia. If that feels wrong, the fix is to cut
   Pressure to 5% and give the 5% to Resource Availability (30%).
2. **Air Profile has the thinnest per-site data.** Dust-storm exposure
   differs by region, but there is no clean per-site dust number for these
   5 sites. Its scores above are approximate, from mission experience
   (e.g. InSight's dust, Gale's dust region). A judge could fairly ask
   for the source of a 3 vs a 4 here.
3. **The Meridiani judgement call survives.** Resource Availability is
   still one number for ice vs ancient minerals, so Meridiani's
   water/resource 4 (hematite/sulfate, not ice) is still a call to make.
4. **Sunlight is gone.** If the team wants solar power scored explicitly,
   swap Air Profile out and put Sunlight back at 10% instead.

## Cost of adopting v2 (4 days before the hackathon)

- Update `SURVIVAL_SCORE.md` + `sites.csv` columns + app score code.
- Rewrite the Oxia pitch line ("top at 80" → "tied top at 78") and the
  demo script's map beat ("Oxia Planum is top at 80" → tie at 78, or
  pick a tie-breaker: Oxia wins on balance, Utopia on water).
- Re-run the combined app and re-check the ranking before the Wed–Thu
  Pogo share.
