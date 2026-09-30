---
title: "Child Poverty by School District: An Interactive Map, 2005 to 2024"
subtitle: A free, interactive map of the share of school-age children in poverty in every U.S. school district, with how each district has changed since 2005.
slug: children-poverty-viz
date: 2026-09-30
time: 19:00:00-04:00
updated: 2026-09-30
prismic_id: aib90RcAAC0A-Wcs
section: Visualization
hero: images/children-poverty-viz-hero-1680x1080.png
hero_alt: Map of the child poverty rate in every U.S. school district in 2024, on a dark background. Districts run from dark red (under 5%) to pale peach (30% or more). The palest areas are in the Mississippi Delta, the Deep South, Navajo Nation lands in Arizona and New Mexico, the Texas border and western Alaska. Small districts are gray. Beside the map: Child Poverty by School District, 14.4% of school-age children lived in families in poverty in 2024. Built by Data 4 The People.
meta_title: "Child Poverty by School District: Map & Trends 2005-2024"
description: "Free interactive map of child poverty in every U.S. school district, 2005 to 2024: yearly rates, which districts got better or worse, and rankings."
keywords: child poverty by school district, child poverty rate by school district, school district poverty rate map, child poverty rate map, child poverty trends by school district, school districts with the highest child poverty rates, child poverty rate visualization, how has child poverty changed over time
schema_type: dataset
dataset_name: Child poverty rates for every U.S. school district, 2005 to 2024, on 2025 district boundaries
dataset_description: "Share of children ages 5 to 17 in families below the official poverty line, for 13,126 U.S. school districts, each year from 2005 to 2024, from the Census Bureau's Small Area Income and Poverty Estimates. Each district's history is tied to its 2025 boundaries: districts that merged are summed from their former districts, and years before a split or redrawing are left out. Includes three-year pooled rates for comparing periods."
temporal: 2005/2024
spatial: United States
measured: Share of children ages 5 to 17 in families below the official poverty line|percent; Number of children ages 5 to 17|count; Number of children ages 5 to 17 in families in poverty|count; Change in three-year pooled child poverty rate|percentage points
sources: https://www.census.gov/programs-surveys/saipe.html|https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html|https://www.census.gov/geographies/mapping-files/time-series/geo/cartographic-boundary.html
distribution: text/html|https://data4thepeople.github.io/ChildPovertyDistrict/;text/csv|https://github.com/Data4ThePeople/ChildPovertyDistrict/tree/main/data/processed
measurement_technique: SAIPE school district estimates matched to the TIGER boundary file each year used; each 2024 district tied to earlier years with 2020 Census blocks weighted by residents under 18, requiring 95% overlap both ways; merged districts summed exactly; rate is children in poverty divided by children ages 5 to 17; change compares three-year pooled rates.
credit: Data 4 The People, from the U.S. Census Bureau
license: https://www.data4thepeople.com/terms-of-use
app_url: https://data4thepeople.github.io/ChildPovertyDistrict/
app_name: "Child Poverty by School District: interactive map, 2005 to 2024"
app_category: EducationalApplication
app_description: Free interactive map of the child poverty rate in every U.S. school district, each year from 2005 to 2024, with change over time and rankings.
app_features: Every U.S. school district, 2005 to 2024|Play through the years at 1x, 2x or 3x|Change between any two three-year periods|Hover or tap any district|History chart for each district|Search any district by name|Filter to one state|Rankings of highest, lowest and largest changes
drop_cap: false
heading_spacer: 20px
caption_spacer: 20px
dividers: false
---

# Child Poverty by School District: An Interactive Map, 2005 to 2024

<iframe src="https://data4thepeople.github.io/ChildPovertyDistrict/?v=20260930#embed=1" width="100%" height="780" loading="lazy" style="border:0" title="Child poverty by school district: interactive map, 2005 to 2024"></iframe>

::: spacer 40px

::: blurb
**[Open the full visualization](https://data4thepeople.github.io/ChildPovertyDistrict/)** **for a larger map, dark mode, and a link you can share to any district.**
:::

::: spacer

::: blurb Updated September 30, 2026
We rebuilt this map with 20 years of history. It now shows every district's child poverty rate for each year from 2005 to 2024, how each district changed over that time, and Vermont, which the first version could not map. The first version, published June 9, 2026, showed 2024 only. [Its method is saved here](https://github.com/Data4ThePeople/ChildPovertyDistrict/blob/main/Child%20Poverty%20by%20School%20District%2C%202024.pdf).
:::

## Purpose

::: spacer

This map shows the share of school-age children living in poverty in every school district in the United States, and how that share has changed since 2005. Pick a year to see the whole country, find your own district, or switch to the change view to see which districts got better and which got worse. The map is free to use and needs no sign-in. It is built from the U.S. Census Bureau's Small Area Income and Poverty Estimates (SAIPE), the only source with a single-year estimate of child poverty for every school district.

We first published this map on June 9, 2026, with 2024 data only. This version is rebuilt from scratch and adds three things. It shows every year from 2005 to 2024. It ties each district's history to its current boundaries, so a district that merged or was redrawn is compared with the same place over time. And it maps all 13,126 districts with a 2024 estimate, including Vermont's 52 supervisory unions.

::: blurb Read this first
This map uses the federal government's official poverty line. A child counts as poor when their family's income before taxes is below a threshold that depends on family size. In 2024 that line was $31,812 a year for two parents and two children, and $25,273 for one parent and two children. The line is the same everywhere in the country, and the income it counts leaves out food stamps (SNAP), housing aid and tax credits. So the map shows children below a bare-bones line, not every child in a family that is struggling to get by. In 2024, 14.3% of all U.S. children under 18 were below the line, and 33.6% were below twice the line ([Census Bureau](https://www2.census.gov/library/publications/2025/demo/p60-287.pdf)).
:::

## Using the visualization

::: spacer

**1. Pick a view.** "One year" colors every district by its child poverty rate in the year you pick. "Change" colors every district by how much its rate went up or down between two periods.

**2. Pick a year.** In the one-year view, drag the Year slider, or click Play to move through every year from 2005 to 2024. The button next to Play sets the speed: 1x, 2x or 3x.

**3. Point at a district.** On a computer, move your mouse over it. On a phone or tablet, tap it. A box shows the district's name, its rate, and the number of children behind it. The District panel on the right shows a chart of the district's rate in every year it has a comparable figure.

**4. Find a district.** Type a name in "Find a district." A list narrows as you type. Pick a name and the map zooms to that district and outlines it.

**5. Pick a state.** The State box zooms the map to one state and limits the rankings to that state.

**6. Zoom and move around.** Use the + and − buttons, scroll with a mouse or trackpad, or pinch on a phone. Drag to move the map. Reset brings everything back to the start.

**7. Compare two periods.** In the change view, pick a From period and a To period. Each period is three years pooled together (see "How to read it" below). Blue districts had a lower rate in the later period. Red districts had a higher rate.

**8. Read the rankings.** The Rankings panel lists the 25 highest and lowest rates for the year you picked, or the 25 largest drops and increases in the change view, nationally or for the state you picked. Click a name to zoom to it.

### How to read it

- **Child poverty rate.** The share of children ages 5 to 17 living in the district who are in families below the official poverty line. It counts children who live in the district, whether they go to a public school, a private school or no school.
- **Pooled rate.** In the change view, each period adds up three years of children in poverty and divides by three years of children. A single year in one district can jump by several points for no real reason. Three years together are steadier. This is our calculation from the Census Bureau's figures.
- **Points.** The change view measures change in percentage points. A district that went from 20% to 15% fell 5 points.
- **Within 2 points.** A change smaller than 2 points either way is shown in gray, because a change that small is well inside the uncertainty of the estimates.
- **Hatched districts.** "No comparable figure" means the district's boundaries in that year were different from today's, so we do not compare it (see Step 4). Older years have more hatched districts.
- **Gray districts.** "Fewer than 100 children" means the district is too small for its rate to be shaded. One family moving in or out can move a small district's rate by several points.
- **High school districts.** In some states, one district runs the elementary schools and another runs the high school. The map colors the elementary district. When you select one, the high school district that serves it is outlined in gray, and its rate is in the District panel.
- **Vermont.** Vermont's estimates are published for supervisory unions, groups of local districts that share one administration, so the map shows those.

### What it shows right now

In 2024, 14.4% of school-age children in the United States lived in families below the poverty line: about 7.9 million of 54.5 million children ages 5 to 17. That rate was 16.5% in 2005, peaked at 20.6% in 2012, and has fallen in most years since.

Across districts, the change was mixed. Comparing 2005 to 2007 with 2022 to 2024, among the 11,499 districts with comparable figures for both periods and at least 100 children, the pooled rate fell by 2 points or more in 3,551 and rose by 2 points or more in 2,385. The districts that fell are home to 28.4% of the children in those districts. The districts that rose are home to 17.2%.

By state, adding up the districts with comparable figures, the pooled rate fell in 40 states and the District of Columbia, and rose in 10. The largest drops were in Montana (4.9 points), Texas (4.0) and the District of Columbia (3.7). The largest increases were in Connecticut (2.3 points), Nevada (1.7) and New Jersey (1.4).

### Highest and lowest

These rankings use 2024 and include only districts with 500 or more children ages 5 to 17. Read them as "near the top" or "near the bottom," not as exact ranks. The estimates for districts this size can be off by many points (see "Honest notes and limitations").

Districts with the highest child poverty rates in 2024:

1. Helena-West Helena School District, AR (66.5%)
2. Atkinson County School District, GA (59.4%)
3. Muskegon Heights School District, MI (57.0%)
4. McLaughlin School District 15-2, SD (54.0%)
5. Greene County School District, AL (53.1%)
6. West Bolivar Consolidated School District, MS (52.9%)
7. Hamtramck Public Schools, MI (52.3%)
8. Clarksdale Municipal School District, MS (52.0%)
9. Pinon Unified District, AZ (52.0%)
10. Greenville Public School District, MS (50.6%)

At the other end, 11 districts had rates of 1.2% or less, eight of them in New Jersey and New York, led by Chesterfield Township School District, NJ (0.9%).

The largest pooled increases from 2005 to 2007 to 2022 to 2024, among districts with 500 or more children a year in both periods, were in Harper Woods City Schools, MI (13.6% to 34.5%), Lanett City School District, AL (23.7% to 40.7%), and Melvindale-North Allen Park School District, MI (19.1% to 34.0%). Several of the largest increases are in older suburbs next to Detroit and Birmingham and in the Youngstown, OH area.

The largest pooled drops were in Indian Oasis-Baboquivari Unified District, AZ (47.4% to 9.7%), Santa Maria Independent School District, TX (64.2% to 26.5%), and Los Fresnos Consolidated Independent School District, TX (55.0% to 22.0%). Six of the ten largest drops are in districts along the Texas border, in the Rio Grande Valley and near El Paso. We treat some of the largest drops with caution. See "Large drops in some places" under "Honest notes and limitations."

## What this page is

::: spacer

Every chart we publish should be something you can check, question and rebuild yourself. This page documents how we built this one: where the data comes from, every step we took, and the judgment calls we made. The code, the data and the built files are in a public repository, linked at the end.

## The data sources

::: spacer

**Small Area Income and Poverty Estimates (SAIPE), school districts, U.S. Census Bureau.** For every school district, every year, the Census Bureau estimates the number of children ages 5 to 17 and the number of those children in families below the official poverty line. We use the national files for 2005 through 2024. Our rate is the second number divided by the first, both from the same row.

**TIGER/Line school district boundaries, U.S. Census Bureau.** The shapes of every unified, elementary and secondary school district, for each year from 2008 to 2025, plus the Census 2010 boundaries. We use them to tell which districts kept the same shape from year to year. From 2022 on, we also use the Census Bureau's administrative district layer, which has Vermont's supervisory unions.

**Cartographic boundary files, 2025, U.S. Census Bureau.** Simplified district and state shapes, trimmed to the shoreline, used only to draw the map.

**2020 Census blocks.** The location of every census block and the number of residents under 18 in each, from the 2020 Census. We use them only to measure how much of a district's population stayed inside the same boundaries from year to year (Step 4).

## How we built it

::: spacer

### Step 0: What the Census Bureau does before we get the data

We start from the Census Bureau's published estimates, so their limits are our limits.

SAIPE numbers are model estimates, not counts. The Census Bureau first estimates the number of poor children in each county, using the American Community Survey, federal tax returns, SNAP records and population estimates. It then splits each county's total among the school districts in it. From 2005 on, that split moves each year with where the low-income child tax exemptions fall on federal tax returns, so a district can improve while its county gets worse.

Before 2005, the split was mostly frozen. For 2001 to 2004, and for 1995 and 1997, each district got a fixed share of its county's total, based on the census before. In those years, a district's change is simply its county's change. That is why this map starts in 2005 (Step 2).

The Census Bureau does not publish a margin of error for each district. It does publish how large the errors typically are for districts of different sizes, which we cover under "Honest notes and limitations."

### Step 1: Rebuild the original

We rebuilt the June map's method in Python from the Census Bureau's 2024 district file. It matches the published figures: 14.4% of children ages 5 to 17 in poverty nationally, and 66.5% in Helena-West Helena School District, AR.

The first version mapped 13,073 districts and could not map 58, mostly in Vermont. Vermont reports its estimates for supervisory unions, which are not in the standard district boundary files. They are in the Census Bureau's administrative district layer, so this version maps all 52. In all, 13,126 of the 13,131 districts with a 2024 estimate are on the map, covering every child in the file except 24. The five left out have 24 or fewer children each.

### Step 2: Pick the years

SAIPE district files go back to 1995, but not every year can show a district changing on its own. We use 2005 to 2024:

- **1995 and 1997:** each district's number is its 1990 Census count times its county's change. Left out.
- **1999 and 2000:** based on the Census 2000 long form, a real district-level measure. We tested 2000 as a starting point and left it out: it sits four years before the rest of the series, uses a different method, and was estimated on boundaries that have no matching file.
- **2001 to 2004:** each district gets a fixed share of its county's total. Left out.
- **2005 to 2024:** each year's split follows that year's tax returns. Used.

### Step 3: Find the boundaries each year used

School district boundaries change. Districts merge, split and trade territory, and a district can keep its ID number through all of it. Each year's SAIPE estimates are made on that year's boundaries, so before comparing a district across years we need to know which boundaries each year used.

We compared the district ID numbers in each SAIPE year with the ID numbers in every boundary file from 2008 to 2025. From 2007 on, each SAIPE year lines up with one boundary file to within a single ID. The file is usually dated one year later: the 2024 estimates are on the 2025 boundaries, not the 2024 ones. The 2005 and 2006 estimates were made on 2005-06 school year boundaries, for which no file exists. For those two years we use the 2008 file and add a check (Step 4).

### Step 4: Tie each district's history to today's boundaries

This is the most important step. A district's rate in 2010 is only comparable with its rate in 2024 if it covered the same place.

To test that, we used the 4.9 million census blocks with children in them, each placed inside its district in every year's boundary file. A 2024 district counts as the same place as a district in an earlier year when at least 95% of its children (measured with 2020 Census block counts) were inside that earlier district, and at least 95% of the earlier district's children are inside today's district. The 95% cutoffs are our judgment call.

Three cases:

- **Same shape.** The district passes the test. Its earlier SAIPE figure is used as published.
- **Merged.** Today's district is made of several whole districts from an earlier year. We add up their SAIPE figures. Because the Census Bureau's counts add up exactly, nothing is estimated. In all, 262 districts have at least one year built this way. Across the year of a merger, the rate moves about as much as it does in an ordinary year.
- **Split or redrawn.** Part of an earlier district became part of today's. We do not estimate these. The district's history starts in the first year its current shape existed.

For 2005 and 2006, which have no matching boundary file, a district must pass the test against both the 2008 and the 2009 files, with the same districts both times. So it counts only if its shape held steady across that gap.

Each district's history runs back from 2024 and stops at the first year that fails. History length varies: some districts go back to 2005, some only a few years, and 29 have 2024 only. That is why older years on the map have more hatched districts. Districts with a comparable figure hold:

- 95.2% of 2024's school-age children in 2005
- 96.8% in 2010
- 98.2% in 2015
- 99.7% in 2020

### Step 5: Draw the map

The colors use the same seven fixed steps as the first version: under 5%, then every 5 points up to 30% or more. They do not rescale to what is on screen, so a 60% district and a 6% district never share a color. On the light map, darker means more children in poverty (in dark mode, brighter means more). Districts with fewer than 100 children are gray, as before.

The shapes come from the Census Bureau's 2025 cartographic files. Vermont's supervisory unions come from its administrative district layer, trimmed to the same shoreline. We simplified every shape so the map loads in a browser, and removed the tiny slivers that simplifying leaves behind. The projection is Albers USA, which moves Alaska and Hawaii into the lower left.

### Step 6: Build the change view

Single years jump. Among districts with 500 or more children, the rate moves by a median of about 1.3 points from one year to the next, and one district in 20 moves 5 to 6 points, with no boundary change behind it. Helena-West Helena went from 44.5% in 2023 to 66.5% in 2024.

So the change view compares three-year periods. Each period's pooled rate is three years of children in poverty divided by three years of children. You can pick any three-year period from 2005 to 2007 through 2022 to 2024, as long as a district has a comparable figure for all three years of both periods. A district needs at least 100 children a year in both periods to be shaded, and at least 500 to be ranked.

### Step 7: Check the numbers

Before publishing, a script recomputes the map's numbers from the Census Bureau's raw files and compares them with what the map shows. Every figure on the map equals the published SAIPE row, or the sum of the published rows of the districts that make it up. The 2024 national rate matches the Census Bureau's file, and the counts in the change view match the map. Every number on this page comes from that output.

## Updating

::: spacer

The Census Bureau releases a new year of school district estimates each winter. We plan to add 2025 when it comes out. Every number on the map is computed by the build scripts.

## Honest notes and limitations

::: spacer

**The official poverty line is narrow.** It counts pretax cash income against a line set in the 1960s and raised only for inflation since, the same in every part of the country. It does not count SNAP, housing aid or tax credits, and it does not subtract rent, child care or medical costs. The Census Bureau's broader measure, the Supplemental Poverty Measure, counts all of these. For children in 2024 it found fewer below the line (13.4%, against 14.3% on the official measure), because tax credits and food aid lift many families over it. It found many more just above it: 49.1% of children had resources below twice their line, against 33.6% on the official measure ([Census Bureau](https://www2.census.gov/library/publications/2025/demo/p60-287.pdf)). This map shows the official line only.

**These are model estimates without district error bars.** The Census Bureau publishes typical error by district size, measured on its 2009 estimates, which it says to treat as an upper bound for 2010 on ([Census Bureau](https://www.census.gov/programs-surveys/saipe/guidance/district-estimates.html)). For districts of 65,000 people or more, which hold 59% of children, a 90% range is about 25% of the estimate either way: New York City's 23.4% is roughly 17.6% to 29.2%. For districts of 5,000 to 10,000 people, it is about 58% either way. Helena-West Helena's 66.5% could be off by about 38 points. Small differences between neighboring districts, and exact ranks, should not be read as real.

**Single years jump.** See Step 6. Read a one-year change in one district with caution, and use the change view for anything longer.

**Large drops in some places.** Several of the largest drops since 2020 are in reservation districts, such as Indian Oasis-Baboquivari, AZ on the Tohono O'odham Nation (40.3% in 2020, 7.2% in 2024). Many of the largest drops since 2005 are in districts along the Texas border. These are the Census Bureau's published numbers, on unchanged boundaries. The model's split among districts leans on federal tax returns, and the expanded Child Tax Credit in 2021 gave families that do not usually file a reason to file. We have not established that this explains the drops. It is a question, not a finding.

**Child counts are not a measure of growth.** District child counts before 2010 rest on Census 2000 shares, and the counts reset when the Census Bureau moved to the 2010 and then the 2020 Census. A district's number of children can jump in 2010 or 2021 for that reason alone.

**Residents, not students.** SAIPE counts children who live in the district, not children enrolled in its schools. Where elementary and high school districts overlap, each district's figure covers only children of its own grade ages.

**Some children are not counted as poor.** Foster children, other children not related to the head of the household, and children living in group homes or institutions are not counted as poor, but they are counted as children. That pulls a district's rate down slightly. We do not know by how much.

**History depends on boundaries.** A district whose boundaries changed has a shorter history on the map, even if the change was small. We chose to leave those years out rather than estimate them.

**The boundaries are simplified.** They are accurate for comparing districts at map scale, not for deciding which district a particular address is in.

## Reproduce it yourself

::: spacer

The code, the build steps and the published files are at [github.com/Data4ThePeople/ChildPovertyDistrict](https://github.com/Data4ThePeople/ChildPovertyDistrict). You need the SAIPE school district files for 2005 to 2024, the TIGER/Line school district files for 2008 to 2025 and Census 2010, the 2025 cartographic boundary files, the 2020 Census block files and block counts of residents under 18, and Python. Every step above is in the scripts, in order. If you get a different number from us, tell us, and we will look.

::: divider

## Common questions

::: spacer

### What poverty line does this map use?

The official federal poverty line. A child counts as poor when their family's income before taxes is below a threshold set by family size. In 2024 it was $31,812 a year for two parents and two children, and $25,273 for one parent and two children. It is nearly the same as the federal poverty guidelines used for program eligibility, $31,200 for a family of four in 2024.

### Does this map undercount child poverty?

It depends on the standard. By the Census Bureau's broader measure, which counts tax credits, food aid and housing aid as well as rent, child care and medical costs, fewer children were below the line in 2024 than on the official measure (13.4% against 14.3%). But many more were just above it: under that measure, 49.1% of children had resources below twice their line. The official line counts children below a bare-bones standard, not every child in a family that is struggling to get by.

### Do other Census Bureau data tell a different story?

Yes, and the difference can be large, especially just above the poverty line. The Census Bureau's American Community Survey (ACS) also reports children by family income for every school district, averaged over five years. It uses the same official poverty line, but its district figures come straight from the survey rather than from the model behind this map, so they can differ. By the ACS, 35.4% of U.S. children ages 6 to 17 lived below twice the poverty line in 2020 to 2024, against about 14% to 16% below the line itself on this map in those years. In some districts the two sources disagree even below the line. For Monte Alto Independent School District, TX, this map shows 26.4% in 2024 and 40.5% for 2020 to 2024 pooled. The ACS puts 67% of its children below the poverty line (give or take 13 points) and 92% below twice the line (give or take 6 points) for 2020 to 2024. Estimates for small districts are uncertain in both sources. We left the ACS off this map until we understand why the two sources differ in places like this.

### How accurate is my district's number?

It is a model estimate, and the Census Bureau does not publish a margin of error for each district. For large districts of 65,000 people or more, the typical range is about 25% of the estimate either way. For small districts it is much wider. Treat small differences between districts, and small changes from one year to the next, with caution.

### Why is my district hatched in earlier years?

Its boundaries in those years were different from today's. We only compare a district with itself when at least 95% of its children lived inside the same boundaries. Districts that merged still have history, because we add up the districts that merged. Districts that were split or redrawn do not.

### Why does my district's rate jump from one year to the next?

Small districts' estimates move a lot from year to year, often with no real change behind them. The change view pools three years at a time to smooth this out.

### Why does the map start in 2005?

Before 2005, the Census Bureau split each county's total among its districts using fixed shares, so a district's change was simply its county's change. From 2005 on, the split follows each year's tax returns.

### Is child poverty going down?

Nationally, the official rate for children 5 to 17 was 16.5% in 2005, peaked at 20.6% in 2012, and was 14.4% in 2024. Across districts it is mixed: comparing 2005 to 2007 with 2022 to 2024, the rate fell by 2 points or more in 3,551 districts and rose by 2 points or more in 2,385.

### Which school district has the highest child poverty rate?

Among districts with 500 or more children, Helena-West Helena School District, AR had the highest estimate in 2024 (66.5%), followed by Atkinson County School District, GA (59.4%) and Muskegon Heights School District, MI (57.0%). The estimates for districts this size can be off by many points, so read these as among the highest, not as exact ranks.

### Why doesn't this match my district's free or reduced-price lunch numbers?

They measure different things. Free and reduced-price lunch counts enrolled students whose families are under 130% or 185% of the poverty guidelines, and in some schools every student eats free under a federal option. This map estimates children who live in the district and are below 100% of the poverty line.

### Why doesn't the number of children match my district's enrollment?

The map counts every child ages 5 to 17 who lives in the district, including those in private school, home school or no school, and leaves out students who live elsewhere.

### Why does Vermont show supervisory unions?

The Census Bureau publishes Vermont's estimates for supervisory unions, groups of local districts that share one administration. The map shows those. Their history before 2021 adds up their member districts.

### Where does the data come from?

The U.S. Census Bureau's Small Area Income and Poverty Estimates for school districts, 2005 to 2024, and its school district boundary files, 2008 to 2025.

### How often is the map updated?

Once a year, after the Census Bureau releases the next year of estimates each winter.

### Can I embed the map?

Yes. It is free to use and embed. Add #embed=1 to the end of the full visualization's address for the 780-pixel version shown on this page.
