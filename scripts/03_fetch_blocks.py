"""2020 Census blocks: interior point (TIGER tabblock20, attribute table only) and
residents under 18 (2020 redistricting data, P1_001N - P3_001N). Blocks with no
children are dropped. Used only to weight boundary overlaps."""
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
import pyogrio
import requests

sys.path.insert(0, os.path.expanduser("~/.claude/d4tp-process"))
from d4tp_env import get_key, load_env  # noqa: E402

from common import RAW, STATES  # noqa: E402

load_env()
KEY = get_key("CENSUS_API_KEY")
OUT = RAW / "blocks"


def county_kids(s, c):
    for i in range(5):
        try:
            r = requests.get("https://api.census.gov/data/2020/dec/pl",
                             params={"get": "P1_001N,P3_001N", "for": "block:*",
                                     "in": f"state:{s} county:{c}", "key": KEY}, timeout=120)
            r.raise_for_status()
            rows = r.json()[1:]
            return [(st + co + tr + bl, int(p) - int(a)) for p, a, st, co, tr, bl in rows]
        except (requests.RequestException, ValueError):
            if i == 4:
                raise
            time.sleep(5 * (i + 1))


def do_state(s):
    dest = OUT / f"{s}.parquet"
    if dest.exists():
        return s, "cached"
    url = f"/vsizip//vsicurl/https://www2.census.gov/geo/tiger/TIGER2020/TABBLOCK20/tl_2020_{s}_tabblock20.zip/tl_2020_{s}_tabblock20.dbf"
    for i in range(10):
        try:
            df = pyogrio.read_dataframe(url, read_geometry=False,
                                        columns=["GEOID20", "COUNTYFP20", "INTPTLAT20", "INTPTLON20", "POP20"])
            break
        except Exception:
            if i == 9:
                raise
            time.sleep(30 * (i + 1))
    df = df[df.POP20 > 0]
    kids = []
    with ThreadPoolExecutor(6) as ex:
        for part in ex.map(lambda c: county_kids(s, c), sorted(df.COUNTYFP20.unique())):
            kids += part
    k = pd.DataFrame(kids, columns=["GEOID20", "kids"])
    m = df.merge(k, on="GEOID20", how="left", validate="1:1")
    if m.kids.isna().any():
        raise ValueError(f"{s}: {m.kids.isna().sum()} populated blocks missing from API")
    m = m[m.kids > 0]
    out = pd.DataFrame({"block": m.GEOID20, "lat": m.INTPTLAT20.astype(float),
                        "lon": m.INTPTLON20.astype(float), "kids": m.kids.astype("int32")})
    OUT.mkdir(parents=True, exist_ok=True)
    out.to_parquet(dest, index=False)
    return s, f"{len(out):,} blocks, {out.kids.sum():,} kids"


def main():
    for s in STATES:
        print(*do_state(s), flush=True)


if __name__ == "__main__":
    main()
