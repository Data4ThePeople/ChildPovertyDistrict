# Datasets

One section per dataset, written before any analysis, updated whenever we learn
something new. The point is to know the traps before they show up in a chart.

Started September 28, 2026.

---

## SAIPE School District Estimates (U.S. Census Bureau)

**What it is.** One row per school district per year: the Census Bureau's
model-based estimate of total population, population ages 5 to 17, and
"relevant related children ages 5 to 17 in families in poverty." Our rate is
the poverty count divided by the 5-to-17 count, both from the same row.

**Where it comes from.**
`https://www2.census.gov/programs-surveys/saipe/datasets/<YYYY>/<YYYY>-school-districts/`.
National file `ussdYY.dat` (1995 to 2002) or `ussdYY.txt` (2003 on), plus
per-state files and an `.xls`. Plain fixed-width text, about 1.7 MB a year, no
login. Each line: state FIPS, 5-digit district ID, name, total population,
population 5 to 17, related children 5 to 17 in poverty, file name, file date.
We read the three numbers from the right of the line, because the name field
changes width across years (35 characters in 1995, 70 in 2000, 72 in 2024).

**Version and vintage.** One release per income year, about 13 months after
the year ends. Years on the server: 1995, 1997, 1999 to 2024 (no 1996 or
1998). The 2024 file is stamped 17FEB2026, and the published post cited the
January 27, 2026 release. The 2024 totals from this file match the published
post exactly (13,131 districts; 54,531,695 children 5 to 17; 7,861,152 in
poverty; 14.4%), so any re-issue did not change the national totals.

**Coverage.** All school districts in the 50 states and DC, on the boundaries
the Census Bureau had for that year (see "Changes over time"). Districts per
year fall from 14,468 (1995) to 13,131 (2024) as districts consolidate.

None of the values are direct counts. How much each year's district number
reflects that district, rather than its county, depends on the method era:

| Estimate years | How the district number is made | Can a district move differently from its county? |
|---|---|---|
| 1995, 1997 | The district's 1990 Census count of poor children, times the county's change since 1990 | No. Census reports average errors up to 60% for small districts in 1995. |
| 1999, 2000 | Census 2000 long-form tabulations for each district piece, pulled toward the county rate by a statistical weighting ("shrinkage"), then made to add up to the SAIPE county total | Yes. This is the closest thing to a measurement in the series. |
| 2001 to 2004 | The same Census 2000 district shares, applied to each year's county total | No. Every district in a county moves with the county. |
| 2005 to 2009 | Census 2000 shares, adjusted each year by where the poor child tax exemptions fell in that year's IRS returns | Yes |
| 2010 to 2024 | That year's IRS child tax exemptions, with 5-year ACS shares and the 2010 (later 2020) Census population base | Yes |

In plain words: the Census Bureau first estimates poverty for each county. It
then splits each county's total among the school districts in it. Before
2005, apart from the census years, the split was frozen at the 2000 (or 1990)
pattern. From 2005 on, the split moves each year with IRS tax records, so a
district can improve while its county gets worse.

What we do with this: the map and change views use **2005 to 2024**. 1995,
1997, and 2001 to 2004 are left out, because in those years a district's
change is its county's change. 1999 and 2000 (Census 2000 based) were in the
first build and were dropped on September 28, 2026 (Eric's call): a lone year
four years before the rest of the series, on a different method and on
boundaries with no TIGER file, added more caveats than it added history.

**Changes over time.**

- Boundaries. Each year is estimated on a specific school-year boundary set:
  1999 and 2000 on 2001-02 boundaries; 2001 to 2003 on 2003-04; 2004 to 2006
  on 2005-06; 2007 and 2008 on 2007-08; 2009 and 2010 on 2009-10 (as revised
  for the 2010 Census). After that, the School District Review Program updated
  boundaries every two years, and every year since 2019. District IDs are
  reused across boundary changes, so the same ID can cover a different area in
  different years. This is the main trap, and the crosswalk (below) exists to
  handle it.
- Inputs. The county model switched from Current Population Survey to American
  Community Survey inputs between 2004 and 2005.
- Population base. District child counts before 2010 lean on Census 2000
  shares. In our first test, district child counts relative to their state
  shift sharply between 2009 and 2010 (share of 2024 children in districts
  whose child count tracks the state within 25%: 75% for 2009, 90% for 2010).
  That is the population base resetting to the 2010 Census, not a boundary
  change. Rates are less affected than counts, but counts before 2010 should
  not be read as a measure of district growth.
- 1995 and 1997: the documentation notes that the numerator and denominator
  refer to slightly different universes, so a true rate cannot be computed.
  Another reason those years are out.
- Name field width and capitalization change (all caps before 2010s, mixed
  case in 2024). Names are not used as keys.

**Suppressed, censored or masked values.** None. Every district gets a number.
Controlled rounding makes districts add up to the county total, so small
districts can show counts like 0 or 1 that are artifacts of rounding.

**Missing data.** No missing-value codes found in 1999 to 2024. Districts with
zero children 5 to 17 exist (rate undefined); we treat them as no data.

**Revisions.** SAIPE does not revise earlier years when methods change. Each
year stays as first published (the 1995 folder has a `correction.txt` and
`revisions.xls`; 1995 is not used). We pin the files as downloaded on
September 28, 2026.

**Units and rounding.** Persons, whole numbers. The whole-number precision is
much finer than the real accuracy, especially for small districts.

**Known quirks.**

- Vermont reports supervisory unions and districts that did not match a 2024
  unified, elementary, or secondary boundary in the original build (58
  unmatched districts). TIGER added an administrative district layer (SDADM)
  in 2022 that may match them. To test.
- Elementary and secondary districts overlap each other by design (a child
  lives in both). They are never summed together.
- A district ID can change type (for example, elementary to unified after a
  merger) while keeping the same number.

**Uncertainty.** The Census Bureau does not publish a margin of error for each
school district. It does publish typical relative error by district size
("Quantifying Relative Error in the School District Estimates",
census.gov/programs-surveys/saipe/guidance/district-estimates.html): the median
coefficient of variation of the count of poor children 5 to 17, measured on
the 2009 estimates, which the Bureau says to treat as an approximate upper
bound for 2010 on. A 90% range is about 1.645 times the CV, as a share of the
estimate:

| District total population | Median CV | Approx. 90% range, share of estimate | 2024 districts | Share of 2024 children | Median range on the 2024 rate |
|---|---|---|---|---|---|
| Under 2,500 | 0.67 | ±110% | 22.8% | 1.1% | ±15.1 points |
| 2,500 to 5,000 | 0.42 | ±69% | 15.0% | 2.1% | ±8.6 points |
| 5,000 to 10,000 | 0.35 | ±58% | 18.1% | 4.9% | ±7.1 points |
| 10,000 to 20,000 | 0.28 | ±46% | 17.3% | 9.0% | ±5.5 points |
| 20,000 to 65,000 | 0.23 | ±38% | 18.5% | 23.5% | ±4.3 points |
| 65,000 and up | 0.15 | ±25% | 8.3% | 59.4% | ±3.0 points |

These are typical values for a size class, not district-specific. Applied to
the rate they are approximate (they describe the count; the 5-to-17
population also carries some error), and a symmetric range stops making
sense near 0% or 100%. Examples for 2024: New York City 23.4% (about 17.6%
to 29.2%); Los Angeles 18.9% (about 14.2% to 23.6%); Helena-West Helena 66.5%
(about ±38 points: its rank as the highest-poverty large district is not
precise). Among districts with 500+ children the median range is about ±5.6
points; 18% exceed ±10. The 25 highest 2024 rates carry ranges of ±11.6 to
±59.5 points. Decision (Eric, September 28, 2026): explain this in the post's
common questions and limits; the map does not show it. For the change view,
no range can be derived (errors in two years are partly shared through the
model), which is one reason for the pooled 3-year rates.

Earlier notes: the Census Bureau publishes no margins of error for school
district estimates. The 1995 documentation reports average errors up to 60%
for small districts and 16% for large ones. Later documentation gives no error
figures for districts. We cannot test whether a change in one district is
statistically real. We use population floors (100 children to shade on the
map, 500 in both years to rank a change) and say that small changes should not
be read as real.

**License and attribution.** U.S. government work, public domain. Credit:
"U.S. Census Bureau, Small Area Income and Poverty Estimates."

---

## TIGER/Line school district boundaries (U.S. Census Bureau)

**What it is.** Polygons for unified (UNSD), elementary (ELSD), and secondary
(SCSD) school districts. From 2022 on, an administrative layer (SDADM) is also
published. GEOID = state FIPS + 5-digit district ID, the same key as SAIPE.

**Where it comes from.** `https://www2.census.gov/geo/tiger/`:
- Census 2000 vintage: `TIGER2010/UNSD/2000/tl_2010_SS_unsd00.zip` (and ELSD,
  SCSD), school year 1999-2000.
- 2008 and 2009: state folders, `tl_200Y_SS_unsd.zip` (ELSD and SCSD only in
  states that have them).
- 2010 to 2025: `TIGER20YY/UNSD|ELSD|SCSD/`, one zip per state.
- Map geometry: cartographic boundary files `cb_2024_us_unsd_500k` and so on
  (generalized for display).

**Version and vintage.** The TIGER release year is not the school year. We
match each SAIPE year to the TIGER vintage whose set of district IDs agrees
best with it, and record the match here once computed.

**Coverage.** 50 states, DC, and territories (we drop territories). There is no
boundary file for school years 2001-02, 2003-04, or 2005-06 unless the 2008
release turns out to carry one of them. To test.

**Changes over time.** Boundaries are redrawn through the School District
Review Program: every two years until 2019, every year after. Districts merge,
split, and trade territory. IDs are sometimes retired and sometimes kept by
the surviving district.

**Known quirks.** TIGER/Line is the full-resolution version. Cartographic
boundary files are simplified and clipped to the shoreline. We use TIGER/Line
for the crosswalk and cartographic files only for drawing.

**Uncertainty.** Boundaries come from state education officials and are
"not survey-grade legal boundaries." The Census Bureau warns against using
them to decide which district an address is in.

**License and attribution.** Public domain. Credit: "U.S. Census Bureau,
TIGER/Line Shapefiles."

---

## 2020 Census blocks and block population under 18 (U.S. Census Bureau)

**What it is.** Used only to measure whether a district is the same place
across years. Each 2020 block has an interior point (INTPTLAT, INTPTLON in the
TIGER `tabblock20` file) and a count of residents under 18 (P1_001N minus
P3_001N in the 2020 redistricting data, via the Census API).

**Where it comes from.** `TIGER2020/TABBLOCK20/tl_2020_SS_tabblock20.zip`;
`api.census.gov/data/2020/dec/pl`.

**Coverage.** Every 2020 block. Under-18 is a stand-in for ages 5 to 17. We
use it only to weight a boundary overlap, never as a published number.

**Known quirks.** 2020 block counts carry the Census Bureau's differential
privacy noise. Individual blocks can be off by a few people. Summed over a
district, the noise is small relative to our 95% overlap threshold.

**License and attribution.** Public domain.

---

## Crosswalk: how district history is stitched to 2024 geography (ours)

This is our construction, not a published dataset. Written up here so the
methodology can draw from it.

1. Each 2020 block with at least one resident under 18 is placed in its
   district for every boundary vintage (point in polygon, separately for
   unified, elementary, and secondary layers).
2. A 2024 district is "the same place" as a district in an older vintage when
   at least 95% of its children (by 2020 blocks) were in that district then,
   and at least 95% of the older district's children are in the 2024 district.
   95% is our judgment call.
3. When a 2024 district is made of whole older districts (a merger), the older
   SAIPE counts are added. The counts add up exactly, so nothing is estimated.
4. Splits and partial territory transfers are not estimated. The district's
   history starts in the first year its current shape existed.
5. Each district gets a "comparable since" year. History length varies by
   district. Some have 20 years (2005 to 2024), some only the most recent. Older maps are sparser. This is by design (Eric, September 28, 2026).

### Which boundaries each SAIPE year used (computed September 28, 2026)

For each SAIPE year we compared its district IDs with every TIGER release
(Vermont and TIGER placeholder codes 999xx left out). From 2007 on, each year
lines up with one release to within a single ID:

| SAIPE years | TIGER release | IDs in SAIPE missing from TIGER / in TIGER missing from SAIPE |
|---|---|---|
| 2000 | Census 2000 (school year 1999-2000) | 39 / 227, approximate |
| 2005, 2006 | 2008 | 271 / 81, approximate |
| 2007, 2008 | 2009 | 1 / 40 |
| 2009, 2010 | 2011 (same as Census 2010) | 1 / 61 |
| 2011, 2012 | 2013 | 1 / 63 |
| 2013, 2014 | 2015 | 1 / 75 |
| 2015, 2016 | 2017 | 1 / 80 |
| 2017 | 2018 | 1 / 86 |
| 2018 to 2024 | 2019 to 2025 (one year later each) | 1 / 82 to 84 |

SAIPE 2024 is on the **2025** TIGER boundaries, not 2024. The published June
2026 map used 2024 TIGER, which may account for a few of its 58 unmatched
districts.

SAIPE 2000 used 2001-02 boundaries and 2005-06 used 2005-06 boundaries. Neither
school year has a TIGER file. For those years a district must pass the test
at the nearest release **and** at the 2009 release with the same component
districts, so it only counts if its shape held steady across the gap.

The TIGER 2017 New Jersey unified file is rejected by the www2.census.gov
firewall ("Request Rejected"); the pipeline falls back to the FTP mirror
(ftp2.census.gov), which serves the same file.

### Results

- 2024: 13,126 of 13,131 SAIPE districts placed on 2025 TIGER geometry,
  covering all but 24 of 54,531,695 children. The five left out have 0 to 24
  children (three Maine unorganized territories and plantations, one Ohio
  island district, one Montana elementary district). All 52 Vermont
  supervisory unions are placed, using the TIGER administrative district
  layer (SDADM). The published map missed 58 districts, mostly Vermont.
- Vermont before 2021 is reported by member districts, not unions. A union's
  history is the sum of its member districts when they fit inside it. 16 of
  52 unions reach back to 2000, 21 to 2005, all 52 by 2023.

Comparable history, by year (share of 2024 districts and of 2024 children
ages 5 to 17):

| Year | Districts | Share of districts | Share of children | Built by adding districts |
|---|---|---|---|---|
| 2024 | 13,126 | 100.0% | 100.0% | 0 |
| 2020 | 13,048 | 99.4% | 99.7% | 28 |
| 2015 | 12,826 | 97.7% | 98.2% | 75 |
| 2010 | 12,430 | 94.7% | 96.8% | 201 |
| 2005 | 12,209 | 93.0% | 95.2% | 233 |
| 2000 | 11,510 | 87.7% | 88.8% | 206 |

Full year-by-year table: `data/processed/` (built by `scripts/06_crosswalk.py`).

Check on merges: across a merger (the year a district's history switches from
a sum of several districts to one), the year-to-year change in the rate looks
like any other year's change (middle 90%: -3.8 to +5.3 points, against -4.3
to +4.1 in years with no change). Adding the counts does not create jumps.

### Year-to-year noise (important for the change view)

Among districts with 500 or more children, the rate moves by a median of
about 1.3 percentage points from one year to the next, and 1 in 20 districts
moves 5 to 6 points, with no boundary change. Example: Helena-West Helena,
Arkansas, 44.5% in 2023 and 66.5% in 2024 (the 2024 figure matches the
published map). Single-year changes in one district should not be read as
real without a longer run behind them.

Two years move more than the rest:

- 2009 to 2010: rates move a median of 2.0 points (99th percentile 14.4). The
  recession and the method switch (IRS plus ACS shares, 2010 Census
  population base) both land here.
- District child counts reset in 2010 (median change 6.5%) and 2021 (5.0%),
  when the population base moved to the 2010 and 2020 Censuses. Counts are
  not a measure of district growth across those years.

---

## Source coverage check (September 28, 2026)

Every SAIPE district value is a model estimate; none is a direct count. What
changes over time is how much of a district's number comes from data about
that district and how much comes from its county:

| Map years | District-level input | Share of 2024 children with a comparable figure |
|---|---|---|
| 2000 | Census 2000 long form for each district piece, pulled toward the county rate | 88.8% |
| 2005 to 2009 | Census 2000 shares, moved each year by that year's IRS child tax exemptions | 95.2% to 96.8% |
| 2010 to 2024 | That year's IRS child tax exemptions plus 5-year ACS shares | 96.8% to 100% |

Years left out because the district number is its county's change applied to
a fixed share: 1995, 1997 (1990 Census shares) and 2001 to 2004 (Census 2000
shares). The Census Bureau publishes no margins of error for district
estimates in any year.

The map shows measured-versus-missing directly: a district with no comparable
figure for a year is hatched, not colored.

### Caveat for the post: large recent drops on reservations

Between 2018-2020 and 2022-2024, 3 of 9,355 districts with 500 or more
children fell by 20 points or more; none rose that much. Several of the
largest drops are reservation districts: Indian Oasis-Baboquivari, AZ
(Tohono O'odham Nation; 42.1% to 9.7%, and 40.3% in 2020 to 7.2% in 2024),
Sacaton, AZ (Gila River; 36.4% to 16.5%), Chinle, AZ (Navajo Nation; 51.4% to
36.9%), St. Ignatius, MT (Flathead; 30.3% to 17.9%). These are the Census
Bureau's published numbers under unchanged district boundaries, so they are
shown as published. The model's district split leans on IRS tax filings, and
filing on reservations may have shifted after the 2021 expanded Child Tax
Credit. We have not established that; it is a question, not a finding. The
post should not present these drops as real change without a check against
another source (for example the ACS 5-year school district tables).

### Poverty definition

SAIPE uses the official poverty measure (pretax cash income against national
thresholds, $31,812 for two parents and two children in 2024). Full
assessment, including the SPM comparison and near-poverty shares:
`analysis/saipe-poverty-definition.md`.

---

## ACS 5-year 2020-2024, table B17024 (U.S. Census Bureau)

**What it is.** Age by ratio of income to poverty level. We use children 6
to 11 and 12 to 17 (the table has no 5-year-old break), total and below 2.00
times their official poverty threshold (the eight bands under 2.00). Same
official thresholds and income definition as SAIPE; see
`analysis/saipe-poverty-definition.md`.

**Where it comes from.** api.census.gov/data/2024/acs/acs5, `group(B17024)`
for school district (unified), (elementary), and (secondary) in every state.
`scripts/10_fetch_acs.py`. Pulled September 28, 2026.

**Coverage.** One period, 2020-2024, pooled survey responses from five
years. Not a series, and not comparable with single-year SAIPE numbers.
Universe is people whose poverty status is determined, which includes some
children SAIPE leaves out of its numerator (unrelated children 6 and older).

**Geography.** ACS 2020-2024 is tabulated on the 2024 TIGER boundaries; the
map uses 2025. `scripts/11_build_acs.py` reuses the crosswalk: 13,039
districts are the same shape and take their row directly; 4 are sums of
former districts; the 52 Vermont unions are sums of their member unified and
elementary districts (ACS has no union geography); 29 districts changed
boundaries between the 2024 and 2025 files and get no ACS figure; 2 had no
ACS row. Where elementary and secondary districts overlap, ACS counts every
child 6 to 17 in each, so sums use only the elementary pieces.

**Uncertainty.** Every estimate has a 90% margin of error. Sums use the
Census Bureau's root-sum-of-squares approximation; the rate's margin uses its
formula for a derived proportion. Typical rate margins: about ±5 points for
districts with 5,000+ children, ±10 for 1,000 to 5,000, ±21 for 100 to 500.
**The map shades a district only when the margin is ±10 points or less and
it has at least 100 children 6 to 17**: 4,939 of 12,738 map districts,
86.1% of children. Others show as "too uncertain." Rankings add a floor of
500 children (5,091 districts) and show each margin.

**Check.** ACS children 6 to 17 against SAIPE children 5 to 17 in unified
districts: median ratio 0.917 (about 12/13, as expected). Gaps in large
single-county districts (Los Angeles, New York City, Miami-Dade), whose
boundaries cannot differ, show that the remaining differences come from the
5-year pooling and sampling, not boundaries.

**National figure.** 35.4% of children 6 to 17 below twice the poverty line
(sum over unified, elementary, and Vermont union districts). The CPS figure
for all children under 18 in 2024 is 33.6% (P60-287, Table B-5); different
survey, ages, and period.

**License.** Public domain.
