"""Charts and numbers for the Day 2 post, six takeaways from the child poverty map (six-takeaways-child-poverty).

Writes PNGs to posts/six-takeaways-child-poverty/images/ in the dark house palette, and the
numbers behind them to data/processed/takeaways_*.csv for the tie-out. Inputs:
  - data/processed/saipe_all_years.csv, district_series.csv, takeaway1_county_gaps.csv (this repo)
  - data/processed/p60_287_children_income_to_poverty.csv: Census P60-287 Table B-5, children,
    2024 (typed from the report, with its page reference)
  - ../laus/data/laus_county_lf.parquet: BLS LAUS county labor force (Eric's labor force viz)
"""
import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from common import PROC, ROOT  # noqa: E402

OUT = ROOT / "posts" / "six-takeaways-child-poverty" / "images"
BG, INK, MUTED, GRID = "#181A1B", "#BBBDC0", "#8C9094", "#2A2E31"
CORAL, BLUE, GOLD, GREEN = "#f37952", "#5598e7", "#eda100", "#1baf7a"
DELTA = {"28011": "Bolivar", "28027": "Coahoma", "28053": "Humphreys", "28055": "Issaquena", "28083": "Leflore",
         "28119": "Quitman", "28125": "Sharkey", "28133": "Sunflower", "28143": "Tunica", "28151": "Washington"}
LAUS = ROOT.parent / "laus" / "data" / "laus_county_lf.parquet"
SOURCE = "Data 4 The People  ·  Source: U.S. Census Bureau, SAIPE school district estimates"

plt.rcParams.update({"text.parse_math": False, "font.family": "DejaVu Sans", "axes.facecolor": BG,
                     "figure.facecolor": BG, "text.color": INK, "axes.labelcolor": INK, "xtick.color": INK,
                     "ytick.color": INK, "axes.edgecolor": GRID})


def fig(title, sub, h=7.5, legend=None):
    """Title, subtitle (may have several lines) and an optional legend row of colored words.
    Returns the figure and the top of the space left for the plot, in figure fraction."""
    f = plt.figure(figsize=(12, h), dpi=150)
    px = 1 / (h * 150)                       # one pixel in figure fraction (height)
    f.text(0.04, 1 - 22 * px, title, fontsize=20, fontweight="bold", va="top")
    y = 1 - 75 * px
    for line in sub.split("\n"):
        f.text(0.04, y, line, fontsize=12.5, color=MUTED, va="top")
        y -= 30 * px
    if legend:
        y -= 8 * px
        x = 0.04
        r = f.canvas.get_renderer()
        for word, color in legend:
            t = f.text(x, y, word, fontsize=12, fontweight="bold", color=color, va="top")
            x += t.get_window_extent(renderer=r).width / f.bbox.width + 0.025
        y -= 30 * px
    return f, y - 22 * px


def finish(f, ax, name, source=SOURCE):
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.tick_params(length=0)
    f.text(0.04, 0.02, source, fontsize=10, color=MUTED)
    f.savefig(OUT / name, facecolor=BG)
    plt.close(f)
    print("wrote", name)


def saipe():
    sa = pd.read_csv(PROC / "saipe_all_years.csv", dtype={"geoid": str})
    sa = sa[sa.year >= 2005].copy()
    sa["r"] = 100 * sa.kids_pov / sa.kids_5_17.replace(0, np.nan)
    return sa


def pooled():
    ser = pd.read_csv(PROC / "district_series.csv", dtype={"geoid": str})
    pk = ser.pivot(index="geoid", columns="year", values="kids_5_17")
    pp = ser.pivot(index="geoid", columns="year", values="kids_pov")
    w0, w1 = [2005, 2006, 2007], [2022, 2023, 2024]
    ok = pk[w0 + w1].notna().all(axis=1)
    a = 100 * pp.loc[ok, w0].sum(1) / pk.loc[ok, w0].sum(1)
    b = 100 * pp.loc[ok, w1].sum(1) / pk.loc[ok, w1].sum(1)
    return pd.DataFrame({"kids24": pk.loc[ok, 2024], "k0": pk.loc[ok, w0].mean(1), "k1": pk.loc[ok, w1].mean(1),
                         "r0": a, "r1": b, "chg": b - a}), ser


# 1. Same county, worlds apart
def t1():
    allg = pd.read_csv(PROC / "takeaway1_county_gaps.csv")
    top = allg.head(10)
    extra = allg[allg.county == "Montgomery County, OH"]   # Dayton, set apart below the top 10 (Eric's county)
    assert len(extra) == 1
    rank = int(allg.index[allg.county == "Montgomery County, OH"][0]) + 1
    g = pd.concat([extra, top.iloc[::-1]]).reset_index(drop=True)   # row 0 (bottom) = Montgomery; widest gap at the top
    f, top_y = fig("Same county, worlds apart",
                   "Child poverty rate, ages 5 to 17, 2024: the highest- and lowest-poverty school district in each county.\n"
                   "Districts with 1,000+ children and 90%+ of them in the county. The 10 widest gaps, plus Montgomery County, OH.", h=9.6,
                   legend=[("Highest-poverty district", CORAL), ("Lowest-poverty district", BLUE)])
    ax = f.add_axes([0.20, 0.09, 0.36, top_y - 0.09])
    y = np.array([0] + [i + 1.0 for i in range(1, len(g))], dtype=float)   # extra gap below the top 10
    ax.hlines(y, g.lo_rate, g.hi_rate, color=GRID, lw=6, zorder=1)
    ax.scatter(g.hi_rate, y, s=110, color=CORAL, zorder=3)
    ax.scatter(g.lo_rate, y, s=110, color=BLUE, zorder=3)
    ax.axhline(1.0, color=MUTED, lw=0.8, ls=(0, (3, 3)))
    ax.set_yticks(y)
    ax.set_yticklabels(g.county, fontsize=11.5, fontweight="bold")
    ax.set_ylim(-0.6, y[-1] + 0.6)
    ax.set_xlim(0, 60)
    ax.set_xticks([0, 20, 40, 60])
    ax.set_xticklabels(["0%", "20%", "40%", "60%"])
    ax.grid(axis="x", color=GRID)
    for yy, r in zip(y, g.itertuples()):
        ax.text(62, yy + 0.17, f"{r.hi_rate:.1f}%  {r.high}", va="center", fontsize=10, color=CORAL, clip_on=False)
        ax.text(62, yy - 0.2, f"{r.lo_rate:.1f}%  {r.low}", va="center", fontsize=10, color=BLUE, clip_on=False)
    ax.text(-0.5, 0.62, f"Also: Montgomery County, OH (Dayton), the {rank}th-widest gap", fontsize=10, color=MUTED, va="center")
    finish(f, ax, "01-same-county-worlds-apart.png")


# 2. Concentrated child poverty
def t2(sa):
    rows = []
    for y, d in sa[sa.kids_5_17 > 0].groupby("year"):
        k = d.kids_5_17.sum()
        rows.append((y, 100 * d.kids_5_17[d.r >= 30].sum() / k, int(((d.r >= 30) & (d.kids_5_17 >= 500)).sum()),
                     100 * d.kids_pov[d.r >= 30].sum() / d.kids_pov.sum(), 100 * d.kids_pov.sum() / k))
    t = pd.DataFrame(rows, columns=["year", "share_kids_30", "districts_30_500", "share_poor_kids_30", "national_rate"])
    t.to_csv(PROC / "takeaways_2_concentration.csv", index=False)
    f, top = fig("Fewer children live in high-poverty districts",
                 "Share of U.S. children ages 5 to 17 who live in a school district where 30% or more of children are in poverty")
    ax = f.add_axes([0.07, 0.1, 0.88, top - 0.1])
    ax.plot(t.year, t.share_kids_30, color=CORAL, lw=3, marker="o", ms=5)
    for y in (2005, 2012, 2024):
        v = t.set_index("year").share_kids_30[y]
        ax.annotate(f"{v:.1f}%", (y, v), xytext=(0, 12), textcoords="offset points", ha="center", fontsize=13, fontweight="bold")
    ax.set_ylim(0, 25)
    ax.set_yticks([0, 5, 10, 15, 20, 25])
    ax.set_yticklabels([f"{v}%" for v in (0, 5, 10, 15, 20, 25)])
    ax.set_xticks([2005, 2008, 2012, 2016, 2020, 2024])
    ax.grid(axis="y", color=GRID)
    finish(f, ax, "02-high-poverty-districts.png")
    return t


# 3. Largest districts
def t3(p, nm):
    t = p.copy()
    t["name"] = nm.reindex(t.index)
    t = t.sort_values("kids24", ascending=False).head(25).sort_values("chg")
    t.to_csv(PROC / "takeaways_3_largest_districts.csv")
    short = {"New York City Department Of Education": "New York City", "Los Angeles Unified School District": "Los Angeles",
             "Dade County School District": "Miami-Dade", "Clark County School District": "Clark County (Las Vegas)",
             "Broward County School District": "Broward County (Fort Lauderdale)", "Hillsborough County School District": "Hillsborough (Tampa)",
             "Houston Independent School District": "Houston", "Orange County School District": "Orange County (Orlando)",
             "Philadelphia City School District": "Philadelphia", "Palm Beach County School District": "Palm Beach County",
             "Hawaii Department of Education": "Hawaii (statewide)", "Wake County Schools": "Wake County (Raleigh)",
             "Fairfax County Public Schools": "Fairfax County, VA", "Charlotte-Mecklenburg Schools": "Charlotte-Mecklenburg",
             "Gwinnett County School District": "Gwinnett County, GA", "Montgomery County Public Schools": "Montgomery County, MD",
             "Dallas Independent School District": "Dallas", "Duval County School District": "Duval (Jacksonville)",
             "Prince George's County Public Schools": "Prince George's County, MD", "Polk County School District": "Polk County, FL",
             "Baltimore County Public Schools": "Baltimore County, MD", "Cypress-Fairbanks Independent School District": "Cypress-Fairbanks (Houston area)",
             "San Diego City Unified School District": "San Diego", "Jefferson County School District": "Jefferson County (Louisville)",
             "Northside Independent School District": "Northside (San Antonio)"}
    f, top = fig("Big cities improved; many suburban districts did not",
                 "Pooled child poverty rate, 2005-2007 to 2022-2024, for the 25 school districts with the most children. Sorted by change.", h=10,
                 legend=[("2005-2007", MUTED), ("2022-2024, lower", BLUE), ("2022-2024, higher", CORAL)])
    ax = f.add_axes([0.30, 0.07, 0.66, top - 0.07])
    y = np.arange(len(t))
    ax.hlines(y, t.r0, t.r1, color=GRID, lw=4)
    ax.scatter(t.r0, y, s=55, color=MUTED, zorder=3)
    col = lambda c: CORAL if round(c, 1) > 0 else BLUE if round(c, 1) < 0 else MUTED
    ax.scatter(t.r1, y, s=70, color=[col(c) for c in t.chg], zorder=4)
    ax.set_yticks(y)
    ax.set_yticklabels([short.get(n, n) for n in t.name], fontsize=11)
    for i, r in enumerate(t.itertuples()):
        ax.text(max(r.r0, r.r1) + 0.8, i, f"{r.chg:+.1f}".replace("-", "\u2212"), va="center", fontsize=10, color=col(r.chg))
    ax.set_xlim(0, 36)
    ax.set_xticks([0, 10, 20, 30])
    ax.set_xticklabels(["0%", "10%", "20%", "30%"])
    ax.grid(axis="x", color=GRID)
    finish(f, ax, "03-largest-districts.png")
    return t


# 4. Industrial Midwest
def t4(p, nm):
    st = {"39": "OH", "26": "MI", "29": "MO", "42": "PA", "36": "NY", "18": "IN", "27": "MN", "06": "CA", "17": "IL"}
    t = p[(p.kids24 >= 5000) & (p.k0 >= 5000)].copy()
    t["name"] = nm.reindex(t.index)
    t = t.sort_values("chg", ascending=False).head(15)
    t.to_csv(PROC / "takeaways_4_largest_increases.csv")
    t = t.iloc[::-1]
    f, top = fig("Where child poverty rose most",
                 "Change in pooled child poverty rate, 2005-2007 to 2022-2024, percentage points. Districts with 5,000+ children in both periods.", h=8.5,
                 legend=[("Ohio, Michigan and the St. Louis area", CORAL), ("Elsewhere", MUTED)])
    ax = f.add_axes([0.40, 0.07, 0.55, top - 0.07])
    mid = t.index.str[:2].isin(["39", "26", "29"])
    ax.barh(np.arange(len(t)), t.chg, color=[CORAL if m else MUTED for m in mid], height=0.68)
    ax.set_yticks(np.arange(len(t)))
    ax.set_yticklabels([f"{n.replace(' School District', '').replace(' Community Schools', '').replace(' Public Schools Community District', '').replace(' Unified', '').replace(' Central', '').replace(' Area', '')}, {st.get(g[:2], g[:2])}"
                        for n, g in zip(t.name, t.index)], fontsize=11)
    for i, r in enumerate(t.itertuples()):
        ax.text(r.chg + 0.2, i, f"+{r.chg:.1f}  ({r.r0:.1f}% to {r.r1:.1f}%)", va="center", fontsize=10)
    ax.set_xlim(0, 21)
    ax.set_xticks([])
    finish(f, ax, "04-largest-increases.png")
    return t


# 6. Official line vs SPM
def t5():
    d = pd.read_csv(PROC / "p60_287_children_income_to_poverty.csv")
    f, top = fig("Just above the line",
                 "Children under 18 by family resources compared with their poverty line, 2024.",
                 legend=[("Official measure", CORAL), ("Supplemental Poverty Measure (SPM)", BLUE)])
    ax = f.add_axes([0.08, 0.12, 0.88, top - 0.12])
    x = np.arange(len(d))
    ax.bar(x - 0.2, d.official, width=0.38, color=CORAL)
    ax.bar(x + 0.2, d.spm, width=0.38, color=BLUE)
    for i, r in enumerate(d.itertuples()):
        ax.text(i - 0.2, r.official + 0.6, f"{r.official:.1f}%", ha="center", fontsize=10.5, color=CORAL)
        ax.text(i + 0.2, r.spm + 0.6, f"{r.spm:.1f}%", ha="center", fontsize=10.5, color=BLUE)
    ax.set_xticks(x)
    ax.set_xticklabels(d.band, fontsize=11)
    ax.set_yticks([])
    ax.axvline(1.5, color=MUTED, ls=(0, (3, 3)), lw=1)
    ax.text(1.55, 38, "the poverty line", color=MUTED, fontsize=10.5)
    finish(f, ax, "06-just-above-the-line.png",
           "Data 4 The People  ·  Source: U.S. Census Bureau, Poverty in the United States: 2024 (P60-287), Table B-5")


# 5. The Delta
def t6(sa, ser, nm):
    ids = ["2800185", "2800186", "2800187", "2800198", "2800750", "2801620", "2801890", "2802040", "2802610",
           "2803810", "2803960", "2804290", "2804680"]   # Delta districts (10 core counties) with history 2005-2024
    s = ser[ser.geoid.isin(ids)]
    assert s.groupby("year").size().eq(len(ids)).all()
    yr = s.groupby("year")[["kids_5_17", "kids_pov"]].sum()
    ms = sa[sa.geoid.str[:2] == "28"].groupby("year")[["kids_5_17", "kids_pov"]].sum()
    us = sa.groupby("year")[["kids_5_17", "kids_pov"]].sum()
    t = pd.DataFrame({"delta": 100 * yr.kids_pov / yr.kids_5_17, "mississippi": 100 * ms.kids_pov / ms.kids_5_17,
                      "us": 100 * us.kids_pov / us.kids_5_17})
    t.to_csv(PROC / "takeaways_6_delta_poverty.csv")
    p = s.pivot(index="geoid", columns="year", values="kids_pov") / s.pivot(index="geoid", columns="year", values="kids_5_17") * 100
    pd.DataFrame({"name": p.index.map(nm), "years_30plus": (p >= 30).sum(1), "min": p.min(1), "max": p.max(1),
                  "r2024": p[2024]}).to_csv(PROC / "takeaways_6_delta_districts.csv")
    f, top = fig("The Mississippi Delta: high child poverty, every year",
                 "Child poverty rate, ages 5 to 17. Delta: the 13 school districts in the 10 core Delta counties\nwith comparable figures for every year from 2005 to 2024.")
    ax = f.add_axes([0.07, 0.1, 0.80, top - 0.1])
    for col, c, lab in (("delta", CORAL, "Mississippi Delta"), ("mississippi", GOLD, "Mississippi"), ("us", BLUE, "United States")):
        ax.plot(t.index, t[col], color=c, lw=3)
        ax.text(2024.4, t[col].iloc[-1], f"{lab}\n{t[col].iloc[-1]:.1f}%", color=c, va="center", fontsize=11, fontweight="bold")
    ax.set_ylim(0, 60)
    ax.set_yticks([0, 20, 40, 60])
    ax.set_yticklabels(["0%", "20%", "40%", "60%"])
    ax.set_xticks([2005, 2010, 2015, 2020, 2024])
    ax.grid(axis="y", color=GRID)
    finish(f, ax, "05a-delta-child-poverty.png")

    lf = pd.read_parquet(LAUS)
    lf = lf[lf.year.between(1990, 2025)]
    def ann(mask):   # annual average labor force per county, summed over the counties in the mask
        return lf[mask].groupby(["year", "fips"]).labor_force.mean().groupby("year").sum()
    dl = ann(lf.fips.isin(DELTA))
    msl = ann(lf.fips.str[:2] == "28")
    usl = ann(lf.fips.str[:2] != "72")
    L = pd.DataFrame({"delta": dl, "mississippi": msl, "us": usl})
    L.to_csv(PROC / "takeaways_6_delta_labor_force.csv")
    idx = 100 * (L / L.loc[1990] - 1)
    f, top = fig("The Delta's workforce has been shrinking for decades",
                 "Change in civilian labor force since 1990, annual average. Delta: the 10 core Delta counties.")
    ax = f.add_axes([0.07, 0.1, 0.80, top - 0.1])
    for col, c, lab in (("delta", CORAL, "Mississippi Delta"), ("mississippi", GOLD, "Mississippi"), ("us", BLUE, "United States")):
        ax.plot(idx.index, idx[col], color=c, lw=3)
        ax.text(2025.4, idx[col].iloc[-1], f"{lab}\n{idx[col].iloc[-1]:+.1f}%".replace("-", "\u2212"), color=c, va="center",
                fontsize=11, fontweight="bold")
    ax.axhline(0, color=MUTED, lw=1)
    ax.set_ylim(-45, 45)
    ax.set_yticks([-40, -20, 0, 20, 40])
    ax.set_yticklabels(["\u221240%", "\u221220%", "0%", "+20%", "+40%"])
    ax.set_xticks([1990, 2000, 2010, 2020, 2025])
    ax.grid(axis="y", color=GRID)
    finish(f, ax, "05b-delta-labor-force.png",
           "Data 4 The People  ·  Source: U.S. Bureau of Labor Statistics, Local Area Unemployment Statistics (county labor force, not seasonally adjusted)")
    return t, idx


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    sa = saipe()
    nm = sa[sa.year == 2024].set_index("geoid").name
    p, ser = pooled()
    t1()
    t2(sa)
    t3(p, nm)
    t4(p, nm)
    t5()
    t6(sa, ser, nm)


if __name__ == "__main__":
    main()


def hero():
    """Hero source: chart 1 re-rendered at 1680x1080 with larger type; `hero pad` adds the border."""
    allg = pd.read_csv(PROC / "takeaway1_county_gaps.csv")
    extra = allg[allg.county == "Montgomery County, OH"]
    rank = int(allg.index[allg.county == "Montgomery County, OH"][0]) + 1
    g = pd.concat([extra, allg.head(10).iloc[::-1]]).reset_index(drop=True)
    f = plt.figure(figsize=(16.8, 10.8), dpi=100)
    f.text(0.03, 0.965, "Same county, worlds apart", fontsize=40, fontweight="bold", va="top")
    f.text(0.03, 0.885, "Child poverty rate, ages 5 to 17, 2024: highest- vs. lowest-poverty school district in the same county",
           fontsize=19, color=MUTED, va="top")
    t = f.text(0.03, 0.835, "Highest-poverty district", fontsize=19, fontweight="bold", color=CORAL, va="top")
    w = t.get_window_extent(renderer=f.canvas.get_renderer()).width / f.bbox.width
    f.text(0.03 + w + 0.025, 0.835, "Lowest-poverty district", fontsize=19, fontweight="bold", color=BLUE, va="top")
    ax = f.add_axes([0.205, 0.075, 0.33, 0.72])
    y = np.array([0] + [i + 1.0 for i in range(1, len(g))], dtype=float)
    ax.hlines(y, g.lo_rate, g.hi_rate, color=GRID, lw=9, zorder=1)
    ax.scatter(g.hi_rate, y, s=230, color=CORAL, zorder=3)
    ax.scatter(g.lo_rate, y, s=230, color=BLUE, zorder=3)
    ax.axhline(1.0, color=MUTED, lw=1, ls=(0, (3, 3)))
    ax.set_yticks(y)
    ax.set_yticklabels(g.county, fontsize=17, fontweight="bold")
    ax.set_ylim(-0.6, y[-1] + 0.6)
    ax.set_xlim(0, 60)
    ax.set_xticks([0, 20, 40, 60])
    ax.set_xticklabels(["0%", "20%", "40%", "60%"], fontsize=15)
    ax.grid(axis="x", color=GRID)
    for yy, r in zip(y, g.itertuples()):
        short = lambda n: n.replace(" Public School District", "").replace(" School District", "").replace(" Community School Corporation", "") \
            .replace(" Community Schools", "").replace(" Public Schools", "").replace(" City", "").replace(" Local", "").replace(" Township Schools", "") \
            .replace(" Borough", "").replace(" Area", "")
        ax.text(62, yy + 0.2, f"{r.hi_rate:.1f}%  {short(r.high)}", va="center", fontsize=16, color=CORAL, clip_on=False)
        ax.text(62, yy - 0.24, f"{r.lo_rate:.1f}%  {short(r.low)}", va="center", fontsize=16, color=BLUE, clip_on=False)
    ax.text(0.5, 0.62, f"Also: Dayton's county, the {rank}th-widest gap", fontsize=15, color=MUTED, va="center")
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.tick_params(length=0)
    f.text(0.97, 0.03, "Data 4 The People  ·  Source: U.S. Census Bureau, SAIPE", fontsize=15, color=MUTED, ha="right")
    out = OUT / "six-takeaways-child-poverty-hero-source.png"
    f.savefig(out, facecolor=BG)
    plt.close(f)
    print("wrote", out.name)
