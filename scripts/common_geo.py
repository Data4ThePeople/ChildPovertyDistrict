"""Boundary vintages and a reader that normalizes TIGER field names across years."""
import re

import geopandas as gpd

from common import RAW

# (vintage key, file year tag, file suffix). Keys sort in time order.
VINTAGES = ([("v2000c", "2010", "00"), ("v2008", "2008", ""), ("v2009", "2009", ""), ("v2010c", "2010", "10")]
            + [(f"v{y}", str(y), "") for y in range(2011, 2026)])
LAYERS = ["unsd", "elsd", "scsd", "sdadm"]


def zip_path(vkey, ytag, suf, st, layer):
    return RAW / "tiger" / vkey / f"tl_{ytag}_{st}_{layer}{suf}.zip"


def read_layer(path, geometry=True):
    """Return GeoDataFrame (or DataFrame) with columns geoid, name, layer (+ geometry)."""
    g = gpd.read_file(f"zip://{path}", engine="pyogrio", read_geometry=geometry)
    cols = list(g.columns)
    lea = next(c for c in cols if re.match(r"^(UNSD|ELSD|SCSD|SDADM)LEA", c))
    stc = next(c for c in cols if re.match(r"^STATEFP", c))
    namec = next(c for c in cols if re.match(r"^NAME", c))
    out = g.assign(geoid=g[stc].astype(str).str.zfill(2) + g[lea].astype(str).str.zfill(5),
                   name=g[namec])
    keep = ["geoid", "name"] + (["geometry"] if geometry else [])
    return out[keep]
