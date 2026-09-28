"""Attach the ACS 2020-2024 below-200%-of-poverty estimate to each 2024 map district.

ACS 5-year 2020-2024 is tabulated on the 2024 TIGER school district boundaries; the map uses
2025. The crosswalk's 2023 result (SAIPE 2023 is on the 2024 boundaries) says which 2024 districts
map to which 2024-boundary districts:
  - same shape: take the ACS row directly
  - built from whole former districts: add up their ACS rows (MOEs by root sum of squares)
  - Vermont unions (no ACS geography): add up their member unified and elementary districts
  - anything else: no ACS figure
Where elementary and secondary districts overlap, ACS counts every child 6-17 in each, so a
district built from both uses only the elementary pieces (the secondary ones cover the same area).
Rate MOE uses the Census Bureau's formula for a derived proportion."""
import glob
import importlib

import numpy as np
import pandas as pd

from common import PROC, RAW

MOE_MAX = 10.0  # shade only when the rate's 90% margin of error is 10 points or less


def main():
    acs = pd.read_csv(PROC / "acs_below200_2020_2024.csv", dtype={"geoid": str}).set_index(["layer", "geoid"])
    xw = pd.read_csv(PROC / "crosswalk.csv", dtype={"geoid": str})
    ser = pd.read_csv(PROC / "district_series.csv", dtype={"geoid": str})
    t24 = ser[ser.year == 2024][["geoid", "layer"]]
    c23 = xw[xw.year == 2023].set_index("geoid").components

    # Vermont unions: member unified + elementary districts on the 2024 boundaries
    cw = importlib.import_module("06_crosswalk")
    asg = pd.concat([pd.read_parquet(f, columns=["kids", "v2025_sdadm", "v2024_unsd", "v2024_elsd"])
                     for f in glob.glob(str(RAW / "assign" / "50.parquet"))], ignore_index=True).fillna(0).astype("int64")
    vt = cw.components(asg, "v2025_sdadm", {"unsd": "v2024_unsd", "elsd": "v2024_elsd"}, ("unsd", "elsd"), False)

    rows = []
    for g, lay in zip(t24.geoid, t24.layer):
        if lay == "sdadm":
            r = vt.get(int(g))
            parts = [(l, f"{c:07d}") for l, c in r[0]] if r else None
            how = "vermont members" if r else "no match"
        elif g in c23.index:
            parts = [tuple(p.split(":")) for p in c23[g].split(";")]
            if any(l == "elsd" for l, _ in parts) and lay != "scsd":
                parts = [p for p in parts if p[0] != "scsd"]
            how = "same" if parts == [(lay, g)] else "sum of former districts"
        else:
            parts, how = None, "boundary changed 2024 to 2025"
        if parts and all(p in acs.index for p in parts):
            a = acs.loc[parts]
            tot, below = a.kids_6_17.sum(), a.below200.sum()
            tm, bm = np.sqrt((a.kids_6_17_moe ** 2).sum()), np.sqrt((a.below200_moe ** 2).sum())
        else:
            tot = below = tm = bm = np.nan
            if parts:
                how = "no ACS row"
        rows.append((g, lay, how, len(parts or []), tot, tm, below, bm))
    d = pd.DataFrame(rows, columns=["geoid", "layer", "how", "n_parts", "kids_6_17", "kids_6_17_moe", "below200", "below200_moe"])
    p = d.below200 / d.kids_6_17
    rad = d.below200_moe ** 2 - p ** 2 * d.kids_6_17_moe ** 2
    rad = np.where(rad < 0, d.below200_moe ** 2 + p ** 2 * d.kids_6_17_moe ** 2, rad)
    d["rate"] = 100 * p
    d["rate_moe"] = 100 * np.sqrt(rad) / d.kids_6_17
    d["shade"] = (d.kids_6_17 >= 100) & (d.rate_moe <= MOE_MAX)
    d.to_csv(PROC / "acs_map.csv", index=False)
    s24 = ser[ser.year == 2024].set_index("geoid").kids_5_17
    k = s24.sum()
    print(d.how.value_counts().to_string())
    print(f"with an ACS figure: {d.rate.notna().sum():,} districts, {s24[d.geoid[d.rate.notna()]].sum() / k:.1%} of children")
    print(f"shaded (MOE <= {MOE_MAX:g} points): {d.shade.sum():,} districts, {s24[d.geoid[d.shade]].sum() / k:.1%} of children")


if __name__ == "__main__":
    main()
