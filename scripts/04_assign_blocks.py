"""Place every 2020 block that has children into its school district for every boundary
vintage and layer. One parquet per state; district IDs stored as int32 (0 = none)."""
import sys
from concurrent.futures import ProcessPoolExecutor

import geopandas as gpd
import pandas as pd

from common import RAW, STATES
from common_geo import LAYERS, VINTAGES, read_layer, zip_path

OUT = RAW / "assign"


def do_state(st):
    dest = OUT / f"{st}.parquet"
    if dest.exists():
        return st, "cached"
    b = pd.read_parquet(RAW / "blocks" / f"{st}.parquet")
    pts = gpd.GeoDataFrame(b[["block", "kids"]], geometry=gpd.points_from_xy(b.lon, b.lat), crs="EPSG:4269")
    out = b[["block", "kids"]].copy()
    for vkey, ytag, suf in VINTAGES:
        for layer in LAYERS:
            p = zip_path(vkey, ytag, suf, st, layer)
            col = f"{vkey}_{layer}"
            if not p.exists():
                continue
            poly = read_layer(p)
            poly = poly[~poly.geometry.is_empty & poly.geometry.notna()]
            pp = pts.to_crs(poly.crs) if poly.crs and not poly.crs.equals(pts.crs) else pts
            j = gpd.sjoin(pp, poly[["geoid", "geometry"]], how="left", predicate="within")
            j = j[~j.index.duplicated(keep="first")]
            out[col] = pd.to_numeric(j["geoid"], errors="coerce").fillna(0).astype("int32").values
    OUT.mkdir(parents=True, exist_ok=True)
    out.to_parquet(dest, index=False)
    return st, f"{len(out):,} blocks, {len(out.columns) - 2} vintage-layers"


if __name__ == "__main__":
    states = sys.argv[1:] or STATES
    with ProcessPoolExecutor(6) as ex:
        for st, msg in ex.map(do_state, states):
            print(st, msg, flush=True)
