"""Tie-out: recompute every number the viz shows or the post may cite, from the raw SAIPE
files and the crosswalk outputs, and check them against each other. Prints a list; exits
non-zero on any mismatch."""
import json
import sys

import pandas as pd

from common import MAP_YEARS, PROC

fails = []


def check(label, got, want):
    ok = got == want
    print(f"{'ok  ' if ok else 'FAIL'} {label}: {got}" + ("" if ok else f" (expected {want})"))
    if not ok:
        fails.append(label)


def main():
    raw = pd.read_csv(PROC / "saipe_all_years.csv", dtype={"geoid": str})
    ser = pd.read_csv(PROC / "district_series.csv", dtype={"geoid": str})
    xw = pd.read_csv(PROC / "crosswalk.csv", dtype={"geoid": str})
    md = json.loads((PROC / "map_data.json").read_text())
    r24 = raw[raw.year == 2024].set_index("geoid")

    print("== 2024 national figures (published post: 14.4%, about 7.9M of 54.4M)")
    k, p = int(r24.kids_5_17.sum()), int(r24.kids_pov.sum())
    print(f"     SAIPE file, all {len(r24):,} districts: {p:,} of {k:,} = {100 * p / k:.1f}%")
    s24 = ser[ser.year == 2024]
    mk, mp = int(s24.kids_5_17.sum()), int(s24.kids_pov.sum())
    print(f"     mapped: {len(s24):,} districts, {mp:,} of {mk:,} = {100 * mp / mk:.1f}%")
    check("2024 mapped rate equals SAIPE rate to 0.1", round(100 * mp / mk, 1), round(100 * p / k, 1))
    check("2024 unmapped children", k - mk, 24)
    check("map_data districts = series districts", len(md["d"]), ser.geoid.nunique())
    check("every mapped district has geometry", sum(1 for d in md["d"] if d["id"] in md["geo"]), len(md["d"]))

    print("== every series value equals the sum of its components in the raw SAIPE file")
    rk = raw.set_index(["year", "geoid"])
    bad = 0
    for r in xw.merge(ser, on=["geoid", "layer", "year"]).itertuples():
        ids = [c.split(":")[1] for c in r.components.split(";")]
        kk = int(rk.loc[[(r.year, i) for i in ids], "kids_5_17"].sum())
        pp = int(rk.loc[[(r.year, i) for i in ids], "kids_pov"].sum())
        bad += (kk != r.kids_5_17) or (pp != r.kids_pov)
    check("series rows not matching raw component sums", bad, 0)
    check("no district-year appears twice", int(ser.duplicated(["geoid", "year"]).sum()), 0)

    print("== map_data series equal district_series")
    yi = {y: i for i, y in enumerate(md["years"])}
    check("map years", md["years"], MAP_YEARS)
    s = ser.set_index(["geoid", "year"])
    mism = 0
    for d in md["d"]:
        for y, i in yi.items():
            v = d["k"][i]
            if v is None:
                mism += (d["id"], y) in s.index
            else:
                row = s.loc[(d["id"], y)]
                mism += (v != row.kids_5_17) or (d["p"][i] != row.kids_pov)
    check("map_data values differing from series", mism, 0)

    print("== coverage by year (share of 2024 children with a comparable figure)")
    K = r24.kids_5_17.sum()
    for y in sorted(MAP_YEARS, reverse=True):
        g = ser[ser.year == y].geoid
        print(f"     {y}: {len(g):,} districts ({100 * len(g) / len(r24):.1f}%), {100 * r24.kids_5_17.reindex(g).sum() / K:.1f}% of children")

    print("== spot checks")
    h = ser[(ser.geoid == "0507680") & (ser.year == 2024)].iloc[0]
    check("Helena-West Helena 2024 rate (published 66.5%)", round(100 * h.kids_pov / h.kids_5_17, 1), 66.5)

    print("== headline numbers in the change view (2005-2007 to 2022-2024, 100+ children a year)")
    w0, w1 = [2005, 2006, 2007], [2022, 2023, 2024]
    piv_k = ser.pivot(index="geoid", columns="year", values="kids_5_17")
    piv_p = ser.pivot(index="geoid", columns="year", values="kids_pov")
    full = piv_k[w0 + w1].notna().all(axis=1)
    a = piv_p.loc[full, w0].sum(1) / piv_k.loc[full, w0].sum(1) * 100
    b = piv_p.loc[full, w1].sum(1) / piv_k.loc[full, w1].sum(1) * 100
    big = (piv_k.loc[full, w0].mean(1) >= 100) & (piv_k.loc[full, w1].mean(1) >= 100)
    chg = (b - a)[big]
    print(f"     districts: {len(chg):,}; fell 2+ points: {(chg <= -2).sum():,}; rose 2+ points: {(chg >= 2).sum():,}")
    check("change-view district count (viz shows 11,499)", len(chg), 11499)
    check("fell 2+ (viz shows 3,551)", int((chg <= -2).sum()), 3551)
    check("rose 2+ (viz shows 2,385)", int((chg >= 2).sum()), 2385)

    if fails:
        print(f"\n{len(fails)} FAILED: {fails}")
        sys.exit(1)
    print("\nall checks passed")


if __name__ == "__main__":
    main()
