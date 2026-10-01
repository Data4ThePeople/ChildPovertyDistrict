# Status

Project: ChildPovertyDistrict
Process: ~/.claude/d4tp-process/PROCESS.md

## Current

Post: children-poverty-viz
Step: 2g
Since: 2026-09-30

## Steps

| Step | What | Confirmed | Notes |
|---|---|---|---|
| 1  | Exploration and analysis | 2026-09-28 | Map 2005-2024 (SAIPE only), crosswalk to 2025 boundaries, tie-out passes; ACS parked |
| 2a | Draft with brackets resolved | 2026-09-30 | Claude-drafted at Eric's request; replaces the June page in place (aib90RcAAC0A-Wcs) |
| 2b | Eric's edit, Claude's look-over | 2026-09-30 | No edits to the Claude draft; confirmed as written |
| 2c | Slice markup | 2026-09-30 | 91 slices, 15 FAQ entries; ACS common question added |
| 2d | Hero 1680x1080 + alt text | 2026-09-30 | 2024 map at hero scale, dark palette; alt 476 characters |
| 2e | SEO | 2026-09-30 | Meta title 56, description 147, 8 keywords; Dataset + WebApplication + FAQPage (16) schema; proposals 1-4 accepted |
| 2f | Pushed to Prismic (draft) | 2026-09-30 | Updated aib90RcAAC0A-Wcs in place (uid children-poverty-viz), Migration Release, 93 slices; published/updated 2026-09-30 6:00 pm EDT |
| 2g | Mailchimp teaser | | |

## Stale

None.

## Log

- 2026-09-28 Step 1 opened. Topic: rebuild the SAIPE child poverty by school district map (published June 9, 2026) with as much history as possible, to show which districts got better or worse. Priority is getting the district mapping right across years; history for about 90% of children beats 99.5% map coverage with less history. Free and reduced lunch join dropped from scope for now (Community Eligibility Provision makes FRL a weak poverty proxy after 2014).
- 2026-09-28 Map years set to 2000 and 2005-2024. 1995, 1997 and 2001-2004 dropped: in those years a district's change is its county's change (Census 2000 or 1990 shares held fixed). Eric agreed. History length may vary by district; older maps allowed to be sparse.
- 2026-09-28 Crosswalk done: 13,126 of 13,131 districts on 2025 TIGER geometry (Vermont recovered), history for 95.2% of children back to 2005 and 88.8% to 2000. Change view to use 3-year pooled rates (2000 stands alone); Eric agreed.
- 2026-09-28 Eric's review of the viz: page locked to the 1200x780 embed size; hover now redraws only outlines (map fills cached); legend moved onto the map and compressed so it clears Florida; 2000 dropped, map runs 2005-2024 (history for 95.2% of children back to 2005); play speed 1x/2x/3x added; Vermont supervisory unions were not drawn (layer code collided with secondary districts), fixed.
- 2026-09-28 Step 1 confirmed by Eric. GitHub Pages turned on (workflow deploys dist/). Next: 2a, needs the slug.
- 2026-09-28 Step 1 reopened: adding an ACS 2020-2024 below-200%-of-poverty toggle. No later steps were confirmed, so nothing is stale.
- 2026-09-28 ACS below-200% view added (2020-2024, B17024): shaded only where the margin of error is 10 points or less (4,939 districts, 86.1% of children). Tie-out passes. Waiting on Eric to re-confirm Step 1.
- 2026-09-28 SAIPE error: no per-district margins; Census publishes typical error by district size (table in DATASETS.md). Eric: cover it in the post's common questions and limits, not on the map.
- 2026-09-28 ACS below-200% view removed from the viz (Eric): SAIPE and ACS disagree below the poverty line in some districts (Monte Alto, TX). Scripts and CSVs parked. Viz back to SAIPE only; tie-out passes.
- 2026-09-28 Step 1 re-confirmed by Eric. Next: 2a, needs the slug.
- 2026-09-28 Step 2a opened. Slug: child-poverty-by-school-district. posts/child-poverty-by-school-district/ created.
- 2026-09-28 2a: Claude-drafted POST.md at Eric's request (visualization page, modeled on lorenz-chart-viz); every number checked against the data. Waiting on Eric's edits.
- 2026-09-28 Eric: replace the June page in place. Slug changed to children-poverty-viz (Prismic document aib90RcAAC0A-Wcs, read from the live page); published and updated dates both September 30, 2026, 7:00 pm EDT; June method PDF archived in the repo and linked from the Updated blurb.
- 2026-09-30 Step 2a confirmed by Eric.
- 2026-09-30 Step 2b confirmed by Eric with no changes to POST.md.
- 2026-09-30 Step 2c opened: slice markup check and convert-only run.
- 2026-09-30 2c: added a common question on how the ACS tells a different story (near poverty; Monte Alto), at Eric's request. Converted again: 91 slices, 15 FAQ entries.
- 2026-09-30 Step 2c confirmed by Eric.
- 2026-09-30 2d: hero rendered from the 2024 map at hero scale (scripts/12_hero.py, dark house palette, viz dark-mode ramp), padded with hero pad; alt text 476 characters; hero check ok.
- 2026-09-30 Step 2d confirmed by Eric.
- 2026-09-30 2e: keyword analysis by search results; meta title (56), description (147), 8 keywords, dataset + app schema written. Four text proposals sent to Eric.
- 2026-09-30 2e: Eric accepted proposals 1-4 (FAQ retitled to 'How has child poverty changed over time?', rankings heading retitled, 'How do I find...' FAQ added, Frozen in 1963 link). 16 FAQ entries.
- 2026-09-30 Step 2e confirmed by Eric.
- 2026-09-30 2f: dry run then publish. Updated draft aib90RcAAC0A-Wcs (uid children-poverty-viz) in the Migration Release; 93 slices; hero uploaded as IA-rk3tY1ANitlBz. Before publishing in Prismic: set author (Eric Pachman) and the Visualization tag, which the update does not carry. Not verified by read-back (no PRISMIC_READ_TOKEN).
- 2026-09-30 2f: published and updated time changed to 6:00 pm EDT (Eric); draft aib90RcAAC0A-Wcs re-pushed.
- 2026-09-30 2f: Eric's replacement sentence in 'Read this first' ("counts as in poverty"); draft re-pushed.
- 2026-09-30 2f: SAIPE definition verified against Census sources; Eric accepted precision edits 1-3 in 'Read this first' (threshold depends on family size and number of children; 'The Census Bureau's 2024 line'; CPS labeled). Draft re-pushed.
- 2026-09-30 Step 2f confirmed by Eric. Open before publishing in Prismic: set author and the Visualization tag.
- 2026-09-30 2g: Eric's email draft placed in EMAIL.md verbatim (placeholders filled from the post); change map rendered for email (01-change-map-email, 155 KB JPG); hero JPG 148 KB; opening claim verified (Census P60-290, official rate 10.2% in 2025, lowest since 1959). Edits proposed in chat.
- 2026-09-30 2g: Eric accepted email edits 1-8; Detroit (DPSCD, 115,752 children, 37.6% to 46.0% pooled) replaces Harper Woods (1,825 children). Detroit numbers not yet in POST.md; proposed adding them.
