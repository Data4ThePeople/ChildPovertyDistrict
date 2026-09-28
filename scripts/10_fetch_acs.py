"""ACS 5-year (2020-2024) table B17024, age by ratio of income to poverty, for every unified,
elementary and secondary school district. Keeps children 6 to 17: total, and below 200% of
poverty (the eight bands under 2.00), with margins of error. MOEs of sums use the Census
Bureau's root-sum-of-squares approximation."""
import os
import sys
import time

import numpy as np
import pandas as pd
import requests

sys.path.insert(0, os.path.expanduser("~/.claude/d4tp-process"))
from d4tp_env import get_key, load_env  # noqa: E402

from common import PROC, RAW, STATES  # noqa: E402

load_env()
KEY = get_key("CENSUS_API_KEY")
YEAR = 2024  # 2020-2024 5-year
GEOS = {"unsd": "school district (unified)", "elsd": "school district (elementary)", "scsd": "school district (secondary)"}
TOTAL = ["B17024_015", "B17024_028"]                                     # 6-11, 12-17
BELOW200 = [f"B17024_{i:03d}" for i in list(range(16, 24)) + list(range(29, 37))]  # under .50 ... 1.85-1.99


def get(st, geo):
    for i in range(6):
        r = requests.get(f"https://api.census.gov/data/{YEAR}/acs/acs5",
                         params={"get": "group(B17024)", "for": f"{geo}:*", "in": f"state:{st}", "key": KEY}, timeout=120)
        if r.status_code == 204 or (r.status_code == 400 and "unknown/unsupported geography" in r.text):
            return None
        if r.status_code == 200:
            rows = r.json()
            return pd.DataFrame(rows[1:], columns=rows[0])
        time.sleep(5 * (i + 1))
    raise RuntimeError(f"ACS request failed: {st} {geo}: {r.status_code} {r.text[:200]}")


def main():
    out = []
    for lay, geo in GEOS.items():
        for st in STATES:
            df = get(st, geo)
            if df is None or df.empty:
                continue
            code = df.columns[-1]
            f = lambda c: pd.to_numeric(df[c], errors="coerce")
            moe = lambda cols: np.sqrt(sum(f(c + "M").clip(lower=0) ** 2 for c in cols))
            out.append(pd.DataFrame({
                "geoid": df["state"] + df[code].str.zfill(5), "layer": lay, "name": df["NAME"],
                "kids_6_17": sum(f(c + "E") for c in TOTAL), "kids_6_17_moe": moe(TOTAL),
                "below200": sum(f(c + "E") for c in BELOW200), "below200_moe": moe(BELOW200)}))
        print(lay, sum(len(o) for o in out if o.layer.iloc[0] == lay), flush=True)
    a = pd.concat(out, ignore_index=True)
    a = a[~a.geoid.str[2:].str.startswith("999")]
    if a.duplicated(["geoid", "layer"]).any():
        raise ValueError("duplicate ACS district rows")
    (RAW / "acs").mkdir(parents=True, exist_ok=True)
    a.to_csv(PROC / "acs_below200_2020_2024.csv", index=False)
    print(f"{len(a):,} districts; children 6-17: {a.kids_6_17.sum():,.0f}")


if __name__ == "__main__":
    main()
