# How SAIPE decides which children are poor, and what it misses

Written September 28, 2026, for the Child Poverty by School District post.
Sources are linked at the end. Numbers are for 2024 unless noted.

## Short answer

SAIPE uses the **official poverty measure**. A child counts as poor when
their family's **pretax cash income** is below the Census Bureau's poverty
threshold for that family's size and number of children. The thresholds are
the same across the country, and they are Mollie Orshansky's 1963 food-budget
formula updated only for inflation. For a family of two parents and two
children, the 2024 line was **$31,812** a year. That is within 2% of the HHS
poverty guideline for a family of four ($31,200). So for practical purposes,
yes: it is the FPL.

Whether that "far undercounts" poor children depends on what you compare it
to, and the answer is not the one the Frozen in 1963 post might suggest:

- **Against the Census Bureau's own modern measure (the SPM), it does not
  undercount.** In 2024 the SPM put child poverty at 13.4%, below the official
  14.3%. For 2021 to 2023, the SPM child rate was lower than the official rate
  in 46 states and DC, and higher in none. The SPM adds housing, medical, and
  work costs, but it also counts tax credits, SNAP, and school lunch, which the
  official measure ignores. For children, the benefits outweigh the costs.
- **Against a "can this family cover the basics" standard, it does
  undercount.** One in three children (33.6%) lived below twice the official
  line in 2024. Under the SPM, it is nearly half (49.1%) below twice the SPM
  line. The SPM finds about as many children *below* the line, and far more
  just above it.

In our view, the accurate framing is that SAIPE counts children below a bare
subsistence line, not children whose families can afford a basic life. The
official line is not an undercount of the poverty the Census Bureau measures.
It is a narrow definition of what poverty is.

## 1. The definition, step by step

**The family is the unit.** Everyone in a family is poor, or no one is.
Income from every related family member is added up. ([SAIPE FAQ])

**The income that counts** is pretax money income: wages, Social Security,
unemployment, cash welfare, child support, and similar cash. It **excludes**
capital gains, noncash benefits (SNAP, housing assistance, Medicaid, school
lunch), and tax credits (EITC, Child Tax Credit). Taxes are not subtracted.
([P60-287], p. 2)

**The line it is compared to** is one of 48 thresholds, set by family size,
number of children under 18, and whether the householder is 65 or older.
Selected 2024 thresholds ([thresh24]):

| Family | 2024 poverty threshold |
|---|---|
| One parent, one child | $21,621 |
| One parent, two children | $25,273 |
| Two parents, two children | $31,812 |
| Two parents, three children | $37,436 |
| Weighted average, family of four | $32,130 |

**How the line was built.** Three times the cost of a minimum food diet in
1963. Since then it has been updated each year by consumer price inflation
(CPI-U) and nothing else. It does not vary by place: the same $31,812 applies
in San Francisco and in the Mississippi Delta. ([P60-287], table comparing
the two measures)

**Thresholds versus the FPL.** The Census thresholds are the statistical
line. The HHS poverty guidelines (what programs call the FPL) are a simplified
version derived from them: $31,200 for a family of four and $25,820 for three
in 2024 ([HHS 2024]). They sit within a few percent of each other.

**Which children SAIPE counts.** The numerator is "related children ages 5
to 17 in families in poverty": children related to the householder by birth,
marriage, or adoption. **Foster children, other unrelated children, and
children in group quarters (institutions, group homes) are never counted as
poor**, but they are in the denominator. That pulls the rate down slightly.
We do not have a count of how many children this affects by district.
([SAIPE overview], [SAIPE FAQ])

**Where the district numbers come from.** SAIPE is a model, not a count. It
estimates each county's poor children from the American Community Survey,
IRS returns, SNAP counts, and other inputs, then splits the county total
among its school districts. The split leans on IRS data: a child exemption
is "poor" when the return's adjusted gross income is below the poverty
threshold for the family size on the return ([SAIPE overview]). Children in
households that do not file taxes do not appear in that signal directly;
they enter only through county totals and ACS-based shares.

## 2. Testing the "undercount" claim

### Against the Supplemental Poverty Measure

The SPM is the Census Bureau's own attempt to fix what the official measure
gets wrong. It uses thresholds based on current spending on food, clothing,
shelter, utilities, phone, and internet, adjusts for local housing costs and
for renting versus owning, and counts benefits and taxes. ([P60-287])

For children in 2024 ([P60-287], Table B-6), here is what each change does
to the child poverty rate, in percentage points:

| Added to family resources | Effect on child rate |
|---|---|
| Refundable tax credits (EITC, refundable CTC) | -5.1 |
| SNAP | -1.9 |
| Social Security | -1.9 |
| School lunch | -0.9 |
| Housing subsidies | -0.9 |

| Subtracted from family resources | Effect on child rate |
|---|---|
| Medical expenses | +2.1 |
| Payroll taxes (FICA) | +2.0 |
| Work expenses, including child care | +1.8 |
| Federal income tax | +0.3 |

The net result: 13.4% of children poor under the SPM, against 14.3% under the
official measure. The same held in 2021 to 2023 across states: 15.1% official
against 10.4% SPM nationally, SPM lower in 46 states and DC, and not
statistically different in California, Maryland, Massachusetts, and New
Jersey ([Census 2024 story]). No state had a higher SPM child rate.

What this means for the post: the argument that the official line "far
undercounts" poor children is not supported by the Census Bureau's own better
measure, at least nationally and by state. What the SPM shows is that the
official line and the safety net have been calibrated against each other: a
family near the line is lifted over it by benefits that the official measure
does not see. That is a critique of the system worth making, but it is a
different one.

### Against a basic-needs standard

The undercount case is strong once the question changes from "below the
line" to "able to cover the basics." Share of children by income relative to
their poverty line, 2024 ([P60-287], Table B-5):

| Income relative to poverty line | Official measure | SPM |
|---|---|---|
| Below 50% (deep poverty) | 6.2% | 3.6% |
| 50% to 99% | 8.1% | 10.1% |
| **Below the line** | **14.3%** | **13.7%** |
| 100% to 149% | 9.8% | 19.1% |
| 150% to 199% | 9.5% | 16.3% |
| **Below twice the line** | **33.6%** | **49.1%** |

(The SPM rows in Table B-5 sum to 13.7% below the line, a little above the
13.4% headline rate; we use the headline for the rate and the table for the
distribution.)

Under the SPM, nearly half of U.S. children live in families with resources
below twice the poverty line. Many programs use 130% to 200% of the FPL as
their cutoff for this reason. Your Frozen in 1963 post makes the housing
version of this point: a family at the 2026 guideline of $33,000 can afford
about $917 a month in rent by the one-third rule.

### Geography

The official line is the same everywhere. The SPM adjusts for housing costs.
In the four states where the SPM and official child rates were not
statistically different (CA, MD, MA, NJ), high housing costs cancel out the
benefits. By inference, SAIPE very likely understates hardship in high-cost
districts and overstates it in low-cost districts, relative to what the SPM
would show. We cannot measure this at the district level: the SPM is not
published below the state.

## 3. Limits specific to SAIPE district estimates

1. **Model estimates, no error bars.** The Census Bureau publishes no margins
   of error for school districts. The 1995 method papers reported average
   errors up to 60% for small districts. Year-to-year movement of 5 or more
   points is common in small districts with no real change behind it
   (see DATASETS.md).
2. **Leans on tax filing.** The split among districts in a county follows
   IRS returns. Areas where many families do not file, or where filing
   changed, can shift. The expanded 2021 Child Tax Credit gave families that
   do not usually file a reason to file. The large post-2021 drops in several
   reservation districts (Indian Oasis-Baboquivari, Sacaton, Chinle) may
   reflect a change like this. We have not established it.
3. **Residents, not students.** SAIPE counts children who live in the
   district, whether they attend public, private, charter, or no school.
   It is not the population a district serves.
4. **Grade span.** Where separate elementary and high school districts
   overlap, each gets only the children in its grade range.
5. **Timing.** 2024 estimates were released in January 2026, and some inputs
   are 5-year ACS averages, so a district's number blends several years.
6. **Excluded children.** Foster children, unrelated children, and children
   in group quarters are never counted as poor (section 1).

## 4. What this suggests for the post

- Say plainly which line SAIPE uses, with the dollar figure: "a family of
  four with two children earning less than $31,812 in 2024 before taxes."
  Readers can judge that number for themselves.
- Avoid saying the map undercounts child poverty as the Census Bureau
  defines it; the SPM does not support that. The stronger, defensible point
  is that the official line counts only children below bare subsistence, and
  one in three children (33.6%) lived below twice that line in 2024.
- If the post should show "near poverty" by district, the source is not
  SAIPE but the ACS 5-year school district tables, which report children by
  ratio of income to poverty (including below 200%). Built September 28,
  2026 as the "Below 200% (ACS)" view, 2020-2024 only, with its own margins
  of error; see DATASETS.md.

## Sources

- [P60-287]: U.S. Census Bureau, *Poverty in the United States: 2024*
  (September 2025), https://www2.census.gov/library/publications/2025/demo/p60-287.pdf
  (Tables B-5, B-6; measures comparison table; text on official and SPM rates).
- [thresh24]: U.S. Census Bureau, *Poverty Thresholds for 2024 by Size of
  Family and Number of Related Children Under 18 Years*,
  https://www2.census.gov/programs-surveys/cps/tables/time-series/historical-poverty-thresholds/thresh24.xlsx
- [HHS 2024]: HHS ASPE, 2024 Poverty Guidelines computations,
  https://aspe.hhs.gov/topics/poverty-economic-mobility/poverty-guidelines/prior-hhs-poverty-guidelines-federal-register-references/2024-poverty-guidelines-computations
- [Census 2024 story]: U.S. Census Bureau, "Differences Between Child Poverty
  Measures May Reflect Variations in State Tax Credits or Noncash Benefits"
  (October 2024), https://www.census.gov/library/stories/2024/10/child-supplemental-poverty-measure.html
- [SAIPE FAQ]: https://www.census.gov/programs-surveys/saipe/about/faq.html
- [SAIPE overview]: 2010 to 2024 Overview of School District Estimates,
  https://www.census.gov/programs-surveys/saipe/technical-documentation/methodology/school-districts/overview-school-district.html
