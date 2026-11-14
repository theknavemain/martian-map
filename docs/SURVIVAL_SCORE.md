# Survival Score — how it works (Person B: Data & Logic)

## The idea in plain English
A pretty place on Mars can still kill you. Our score asks 6 survival questions about
every site, gives each answer a mark from 1 (bad) to 5 (good), and combines them
into one score out of 100. Resources count most, because on Mars water = drinking,
oxygen, and even rocket fuel. Then temperature/radiation, terrain, hazards, and the
two new factors from the notebook: pressure and air profile.

## v2 — live since Tue 10 Nov 2026 (adopted from the notebook list)
v1 (water 30% + terrain 25% + temperature 20% + hazard safety 15% + sunlight 10%)
is retired. Sunlight was dropped on purpose: it is mostly driven by latitude,
which Temperature already captures — keeping temperature + sunlight + radiation
would count latitude three times.

## The 6 factors and their weights
| Factor | Question it answers | Weight |
|---|---|---|
| Resource Availability | Can we get water and useful minerals here — ice, or water-rich clays/minerals? | 25% |
| Temperature / Radiation | Warm enough, and shielded enough from cosmic radiation? | 20% |
| Terrain | Is it flat and safe enough to land and build on? | 20% |
| Hazards | How *few* dangers are there (rocks, cliffs, dust traps)? 5 = very safe | 15% |
| Pressure | Atmospheric pressure from elevation — lower ground = thicker air = easier landing + more shielding | 10% |
| Air Profile | Dust and wind — dust storms, dust build-up on panels, wind-blown grit | 10% |

## The formula
```
survival_score = (resource*0.25 + temp_radiation*0.20 + terrain*0.20
                  + hazards*0.15 + pressure*0.10 + air*0.10) * 20
```
Multiplying by 20 turns the 1–5 average into a score out of 100.
This is exactly the `score.py` logic — keep this doc and the code matching.

## How the two new factors are scored

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

### Air Profile — dust and wind (weakest data — say so to judges)
No clean per-site dust number exists for these 5 sites. Scores come from
mission experience: Jezero 4 (dust, moderate), Gale 3 (edge of a
high-dust-cover region; dust devils), Elysium 3 (dust build-up ended
InSight), Oxia 4 (wind ripples, moderate dust), Utopia 3 (northern-plains
dust). A judge could fairly ask for the source of a 3 vs a 4 here.

## Mission profiles (Layers 7 and 9 — in the app, not in the stored score)

The stored v2 score always uses the weights above. The sliders and the
mission planner only re-weight the *same six factors* for one visitor's
mission, and the rules are shown in the app:

- a top priority's weight is doubled
- a mission of 300+ sols raises the resources weight by half again
- a crew of 5+ raises the hazards/safety weight by half again

Weights are normalized, so the result is still out of 100. The survival
kit is built from a site's own weak factors: 1–2 is a critical item, 3 is
standard, 4–5 is basic gear — and the biggest threat is the site's single
lowest factor (ties broken towards the most lethal: temperature/radiation,
then air, hazards, terrain, pressure, resources).

## Scoring guide (use the SAME scale for every new site)
- **5** = excellent for survival (e.g. a known buried ice deposit; a plain chosen for landing safety; ground below −4,000 m)
- **4** = good (e.g. strong evidence of ancient water / clays; mostly flat)
- **3** = average / mixed (e.g. ancient lake minerals but no ice; flat area but rough surroundings)
- **2** = poor (e.g. little water evidence; rocky terrain; high-latitude cold)
- **1** = very poor (no water signs at all / extremely rough / polar cold)

Rule: every score must have a reason in the site's `description`, `water_ice`,
or `elevation_m` field, from the source. No guessing — judges WILL ask
"why did this site get 3 for water?"

## Worked example — Oxia Planum (score: 78)
- Resource 4 → extensive clays formed with ancient water, evidence of groundwater
- Temperature/Radiation 4 → 18°N, near-equatorial; radiation 3 (elevation ~−2,000 m)
- Terrain 4 → wide, low, relatively smooth plain (some wind ridges)
- Hazards 4 → few major hazards; wind ripples are the main travel problem
- Pressure 3 → elevation ~−2,000 m
- Air 4 → wind ripples, moderate dust
- (4×0.25 + 4×0.20 + 4×0.20 + 4×0.15 + 3×0.10 + 4×0.10) × 20 = 3.90 × 20 = **78**

## Results (from sites.csv, v2)
| Site | Score | One-line verdict |
|---|---|---|
| Oxia Planum | 78 | Best all-rounder — tied top with Utopia |
| Utopia Planitia | 78 | Best water on Mars, worst cold — tied top |
| Elysium Planitia | 70 | Safest landing, but weak on resources |
| Gale Crater | 68 | Good all-round, rougher terrain |
| Jezero Crater | 62 | Best science, hardest living |

Top of the list is now a TIE at 78 (Oxia + Utopia). Tie-breaker for the
pitch: Oxia wins on balance (no factor below 3 except pressure), Utopia
wins on water alone (resource 5, the only 5 on the list). Jezero is still
the lowest — "the most famous site is NOT the best place to survive"
still holds.

## Honest caveats (tell the judges these, don't hide them)
1. **Elevation is counted twice.** Low ground wins Pressure (10%) AND part
   of Temperature/Radiation (30% of 20%). That is most of why Utopia
   jumps 71 → 78 and ties Oxia.
2. **Air Profile has the thinnest per-site data** (see above).
3. **The Meridiani judgement call survives.** Resource Availability is
   still one number for ice vs ancient minerals, so Meridiani's
   resource 4 (hematite/sulfate, not ice) is still a call to make — and
   the rows 6–10 draft is still scored on v1, so it must be re-scored
   on v2 before any merge.

## Python code (drop this in score.py later)
```python
def survival_score(resource, temp_radiation, terrain, hazards, pressure, air):
    return round((resource*0.25 + temp_radiation*0.20 + terrain*0.20
                  + hazards*0.15 + pressure*0.10 + air*0.10) * 20)
```

## Your next steps (Person B)
1. Check the 5 rows in sites.csv against the source links — tell me any score you would change, and why.
2. Re-score the rows 6–10 draft on v2 before any merge (it is still v1-scored).
3. Never change a weight without updating this doc AND the app code together.
