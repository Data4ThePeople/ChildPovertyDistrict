"""Build the map data file: district series aligned to the map years, plus simplified,
projected geometry (Albers USA) for the 2024 districts.

Fill layer: unified + elementary districts, and Vermont supervisory unions (from the TIGER
administrative layer, clipped to Vermont's cartographic outline). Secondary districts overlap
elementary ones; their geometry is kept for highlighting but not filled.
Output: data/processed/map_data.json"""
import glob
import json

import geopandas as gpd
import numpy as np
import pandas as pd
import pyarrow.parquet as pq
import shapely

from albers import project
from common import MAP_YEARS, PROC, RAW, STATES

# one-letter layer codes used by the page (sdadm must not collide with scsd)
LAYER_CODE = {"unsd": "u", "elsd": "e", "scsd": "s", "sdadm": "v"}
TOL = 250          # simplification tolerance, meters
GRID = 50          # coordinate grid, meters
MIN_PART = 0.05e6  # drop detached parts under 0.05 km2 after simplification (unless it is the only part)

STATE_INFO = {"01": ("AL", "Alabama"), "02": ("AK", "Alaska"), "04": ("AZ", "Arizona"), "05": ("AR", "Arkansas"),
              "06": ("CA", "California"), "08": ("CO", "Colorado"), "09": ("CT", "Connecticut"),
              "10": ("DE", "Delaware"), "11": ("DC", "District of Columbia"), "12": ("FL", "Florida"),
              "13": ("GA", "Georgia"), "15": ("HI", "Hawaii"), "16": ("ID", "Idaho"), "17": ("IL", "Illinois"),
              "18": ("IN", "Indiana"), "19": ("IA", "Iowa"), "20": ("KS", "Kansas"), "21": ("KY", "Kentucky"),
              "22": ("LA", "Louisiana"), "23": ("ME", "Maine"), "24": ("MD", "Maryland"),
              "25": ("MA", "Massachusetts"), "26": ("MI", "Michigan"), "27": ("MN", "Minnesota"),
              "28": ("MS", "Mississippi"), "29": ("MO", "Missouri"), "30": ("MT", "Montana"),
              "31": ("NE", "Nebraska"), "32": ("NV", "Nevada"), "33": ("NH", "New Hampshire"),
              "34": ("NJ", "New Jersey"), "35": ("NM", "New Mexico"), "36": ("NY", "New York"),
              "37": ("NC", "North Carolina"), "38": ("ND", "North Dakota"), "39": ("OH", "Ohio"),
              "40": ("OK", "Oklahoma"), "41": ("OR", "Oregon"), "42": ("PA", "Pennsylvania"),
              "44": ("RI", "Rhode Island"), "45": ("SC", "South Carolina"), "46": ("SD", "South Dakota"),
              "47": ("TN", "Tennessee"), "48": ("TX", "Texas"), "49": ("UT", "Utah"), "50": ("VT", "Vermont"),
              "51": ("VA", "Virginia"), "53": ("WA", "Washington"), "54": ("WV", "West Virginia"),
              "55": ("WI", "Wisconsin"), "56": ("WY", "Wyoming")}


def prep(geom, st):
    """Project, simplify, prune slivers."""
    g = shapely.simplify(project(shapely.make_valid(geom), st), TOL, preserve_topology=True)
    parts = [p for p in getattr(g, "geoms", [g]) if p.geom_type == "Polygon" and not p.is_empty]
    if len(parts) > 1:
        big = [p for p in parts if p.area >= MIN_PART]
        parts = big or [max(parts, key=lambda p: p.area)]
    return parts


def encode(parts):
    """[[ring, ring...], ...] with each ring a flat delta-encoded int list on the GRID."""
    out = []
    for p in parts:
        rings = []
        for ring in [p.exterior, *p.interiors]:
            xy = np.round(np.asarray(ring.coords)[:-1] / GRID).astype(np.int64)
            keep = np.r_[True, np.any(np.diff(xy, axis=0) != 0, axis=1)]
            xy = xy[keep]
            if len(xy) < 3:
                continue
            d = np.vstack([xy[:1], np.diff(xy, axis=0)])
            d[:, 1] *= -1  # screen y points down
            rings.append(d.ravel().tolist())
        if rings:
            out.append(rings)
    return out


def main():
    series = pd.read_csv(PROC / "district_series.csv", dtype={"geoid": str})
    xw = pd.read_csv(PROC / "crosswalk.csv", dtype={"geoid": str})
    saipe = pd.read_csv(PROC / "saipe_all_years.csv", dtype={"geoid": str})
    names = saipe[saipe.year == 2024].set_index("geoid").name
    layer = series.drop_duplicates("geoid").set_index("geoid").layer
    yi = {y: i for i, y in enumerate(MAP_YEARS)}

    # series arrays
    rec = {}
    for gid, g in series.groupby("geoid"):
        k = [None] * len(MAP_YEARS)
        p = [None] * len(MAP_YEARS)
        for r in g.itertuples():
            k[yi[r.year]] = int(r.kids_5_17)
            p[yi[r.year]] = int(r.kids_pov)
        rec[gid] = {"id": gid, "n": names[gid], "s": gid[:2], "l": LAYER_CODE[layer[gid]], "k": k, "p": p}
    # history notes: earliest year whose value is a sum of several former districts
    multi = xw[xw.components.str.contains(";")]
    for gid, g in multi.groupby("geoid"):
        rec[gid]["m"] = int(g.year.max())

    # elementary -> secondary district that holds most of its children (2025 boundaries)
    asg = pd.concat([pd.read_parquet(f, columns=["kids", "v2025_elsd", "v2025_scsd"])
                     for f in glob.glob(str(RAW / "assign" / "*.parquet"))
                     if {"v2025_elsd", "v2025_scsd"} <= set(pq.read_schema(f).names)], ignore_index=True)
    a = asg[(asg.v2025_elsd > 0) & (asg.v2025_scsd > 0)]
    hs = a.groupby(["v2025_elsd", "v2025_scsd"]).kids.sum().reset_index().sort_values("kids")
    hs = hs.drop_duplicates("v2025_elsd", keep="last")
    for e, s in zip(hs.v2025_elsd, hs.v2025_scsd):
        e, s = f"{int(e):07d}", f"{int(s):07d}"
        if e in rec and s in rec:
            rec[e]["hs"] = s

    # geometry
    geo = {}
    lay_frames = {lay: gpd.read_file(f"zip://{RAW / 'cb' / f'cb_2025_us_{lay}_500k.zip'}") for lay in ("unsd", "elsd", "scsd")}
    vt_outline = shapely.union_all([g for lay in ("unsd", "elsd") for g in
                                    lay_frames[lay][lay_frames[lay].STATEFP == "50"].geometry])
    for lay, g in lay_frames.items():
        for gid, st, geom in zip(g.GEOID, g.STATEFP, g.geometry):
            if gid in rec and st in STATE_INFO:
                geo[gid] = encode(prep(geom, st))
    vt = gpd.read_file(f"zip://{RAW / 'tiger' / 'v2025' / 'tl_2025_50_sdadm.zip'}")
    lea = next(c for c in vt.columns if c.startswith("SDADMLEA"))
    for code, geom in zip(vt[lea], vt.geometry.to_crs(4269)):
        gid = "50" + str(code).zfill(5)
        if gid in rec:
            geo[gid] = encode(prep(shapely.intersection(geom, vt_outline), "50"))
    missing = [g for g in rec if g not in geo]
    print(f"{len(rec):,} districts with data, {len(geo):,} with geometry; no geometry: {missing}")

    st = gpd.read_file(f"zip://{RAW / 'cb' / 'cb_2025_us_state_500k.zip'}")
    st = st[st.STATEFP.isin(STATES)]
    borders = [encode([ring for ring in prep(geom, s)]) for geom, s in zip(st.geometry, st.STATEFP)]

    out = {"years": MAP_YEARS, "grid": GRID,
           "states": {k: v for k, v in STATE_INFO.items()},
           "d": sorted(rec.values(), key=lambda r: r["id"]),
           "geo": geo, "borders": borders}
    dest = PROC / "map_data.json"
    dest.write_text(json.dumps(out, separators=(",", ":")))
    print(f"wrote {dest.name}: {dest.stat().st_size / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
