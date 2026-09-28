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

What we do with this: the map and change views use **2000, then 2005 to
2024**. 1995, 1997, and 2001 to 2004 are left out, because in those years a
district's change is its county's change. 1999 and 2000 rest on the same
Census 2000 data; we use 2000.

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

**Uncertainty.** The Census Bureau does not publish margins of error for school
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
   district. Some have 21 years of data points (2000, 2005 to 2024), some have
   none. Older maps are sparser. This is by design (Eric, September 28, 2026).

Results, match tables, and coverage by year get added here as they are
computed.
