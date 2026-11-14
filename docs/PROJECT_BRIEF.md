# PROJECT BRIEF — copy-paste this into any other AI/tool

---

## PART 1: PROJECT DESCRIPTION (in my POV)

I am Satyam, a BTech student in Computer Science & Engineering (AI) currently in my 3rd semester. Together with my friend and teammate, I am participating in the NASA Space Apps Challenge 2026 (hackathon weekend: 14–15 November 2026, submission deadline 15 November 2026). We are a beginner team of two — we are still learning and this is our first major project, so everything must be simple, realistic, and finishable by two beginners in a hackathon weekend, with about 3 weeks of preparation before it.

Our chosen challenge is **"Interplanetary Survival Guide: Martian Map"** from the NASA Space Apps Challenge 2026.

**Project idea in one line:** We are building an interactive map of Mars that does not just show places — it tells a future astronaut where they could survive, and why.

**What our app does (our MVP):**
1. An interactive Mars map with clickable markers for 12–15 real sites (for example: Jezero Crater, Gale Crater, Elysium Planitia, Oxia Planum, Utopia Planitia, Hellas Planitia, Arcadia Planitia, Mawrth Vallis, Meridiani Planum, and Planum Boreum / the North Pole).
2. A detail card for each site showing: mission that visited/planned for it, terrain, temperature notes, water/ice evidence, hazards, and a short plain-English description — every fact backed by a source link (NASA/JPL/USGS/ESA).
3. A **Survival Score out of 100** for each site, calculated from 5 factors scored 1–5:
   - Water access — 30%
   - Terrain safety/flatness — 25%
   - Temperature favourability — 20%
   - Hazard safety (5 = safest) — 15%
   - Sunlight for solar power — 10%
   Formula: `(water×0.30 + terrain×0.25 + temperature×0.20 + hazard_safety×0.15 + sunlight×0.10) × 20`
4. A **compare view** where a user can compare two sites side by side (including their Survival Scores).
5. A **Survival Guide panel**: for the selected site, "If you landed here, you would need…" (e.g. water supply, heating, radiation shelter, dust protection).

Stretch goal (only if the MVP is fully working): a simple route planner between two sites.

**Our first results so far:** Oxia Planum scores 80, Elysium Planitia 79, Utopia Planitia 71, Gale Crater 68, and Jezero Crater 61. Our favourite insight for the pitch: the most famous site, Jezero, is NOT the best place to survive — our map explains why (great science, rough terrain, no easy ice).

**Data sources we use:** NASA/JPL mission pages and press kits (Perseverance, Curiosity, InSight), NASA's SWIM subsurface water-ice maps, NASA Mars Trek, USGS Astrogeology MOLA elevation data, HiRISE images (University of Arizona), and ESA material for Oxia Planum/ExoMars. We never invent data — every site fact has a source.

**Tech stack (kept beginner-friendly):** Python, Streamlit for the app, Folium for the map, Pandas + a CSV file (`sites.csv`) for our data, GitHub for code sharing and version control. No React, no complex backend, no database.

**Team roles:**
- **Me (Satyam) — Person B, Data & Logic:** the sites dataset (sites.csv), researching and fact-checking every site, designing and coding the Survival Score, the Survival Guide text, the project write-up, pitch and demo script.
- **My teammate — Person A, Map & UI:** the Streamlit app, Folium map, markers/popups, site detail and compare views, layout/styling, and deployment.

We are starting as a team of two. (Do not add plans for extra team members.)

**Timeline:**
- Week 1 (23–30 Oct 2026): learn GitHub + Streamlit basics; working v0 (map with a test pin + first 5 sites in the CSV).
- Week 2 (31 Oct – 6 Nov 2026): build the full MVP (all sites, scores, compare view, survival guide).
- Week 3 (7–13 Nov 2026): polish, bug-fixing, deployment, project page, pitch and demo preparation.
- Hackathon (14–15 Nov 2026): final fixes only, demo, and submit before 15 Nov 11:59 PM local time.

---

## PART 2: INSTRUCTIONS — how to help me

When helping me with this project, follow these rules:

1. **Assume I am a beginner.** Explain things in simple, step-by-step language. Define any technical or space-science term the first time you use it. Prefer small, working examples over theory.
2. **Keep everything within our scope.** Our MVP is listed above. Do not suggest advanced features (real-time NASA APIs, 3D engines, React, machine-learning models, databases) unless I ask. If you suggest an improvement, say clearly whether it is MVP, stretch, or out of scope.
3. **Never invent Mars data.** Coordinates, temperatures, water/ice claims, and mission facts must come from real sources (NASA, JPL, USGS, ESA, or peer-reviewed papers). Always give me the source link for a fact, and mark clearly if something is our own estimate/scoring judgement rather than a measured fact.
4. **Use our stack.** Give code in Python for Streamlit + Folium + Pandas, reading from `sites.csv` with these columns: name, latitude, longitude, mission, terrain, temperature_notes, water_ice, hazards, description, source_url, water_score, terrain_score, temperature_score, hazard_safety_score, sunlight_score, survival_score.
5. **Respect our Survival Score.** Use the exact formula and weights given above. If you score a new site, score all 5 factors 1–5 using this guide: 5 = excellent, 4 = good, 3 = average/mixed, 2 = poor, 1 = very poor — and give a one-line reason for each factor, backed by a source.
6. **Write in my voice where asked.** Project descriptions, pitch text, and the project page should be in first person plural ("we built…") or first person for my personal parts, in simple, confident student English — not corporate/marketing language.
7. **Help me prepare for judges.** When giving me content, also give me: (a) 2–3 judge questions I may be asked about it, and (b) a short model answer for each, in the format fact → so-what-for-survival.
8. **Deliver in small steps.** End each answer with the single next action I should take, sized so a 3rd-semester student can finish it in one sitting (under ~1 hour).

My immediate priorities right now are: (1) reviewing and expanding sites.csv from 5 to 12–15 sites, (2) understanding Mars survival science deeply enough to answer judge questions, and (3) helping my teammate connect the CSV to the map.
