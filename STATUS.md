# Status

Project: ChildPovertyDistrict
Process: ~/.claude/d4tp-process/PROCESS.md

## Current

Post: none yet
Step: 1 (reopened)
Since: 2026-09-28

## Steps

| Step | What | Confirmed | Notes |
|---|---|---|---|
| 1  | Exploration and analysis | 2026-09-28 | Map 2005-2024, crosswalk to 2025 boundaries, tie-out passes |
| 2a | Draft with brackets resolved | | |
| 2b | Eric's edit, Claude's look-over | | |
| 2c | Slice markup | | |
| 2d | Hero 1680x1080 + alt text | | |
| 2e | SEO | | |
| 2f | Pushed to Prismic (draft) | | |
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
