"""Download TIGER/Line school district boundaries for every vintage we test against,
plus the 2024 cartographic boundary files used to draw the map."""
import re
import time
from concurrent.futures import ThreadPoolExecutor

import requests

from common import RAW, STATES, UA, fetch

T = "https://www2.census.gov/geo/tiger"
LAYERS = ["unsd", "elsd", "scsd"]


def get_text(url):
    for i in range(10):
        r = requests.get(url, headers={"User-Agent": UA}, timeout=60)
        if r.status_code == 200:
            return r.text
        print(f"{r.status_code} on listing {url}, retry {i + 1}", flush=True)
        time.sleep(15 * (i + 1))
    raise RuntimeError(f"listing failed: {url}")


def state_folders(year):
    html = get_text(f"{T}/TIGER{year}/")
    return {m[:2]: m for m in re.findall(r'href="(\d\d_[A-Z_]+)/"', html)}


_listing = {}


def listed(url_dir):
    """Set of file names in a Census directory listing (cached)."""
    if url_dir not in _listing:
        _listing[url_dir] = set(re.findall(r'href="([^"/?]+\.zip)"', get_text(url_dir)))
    return _listing[url_dir]


def jobs():
    out = []
    # Census 2000 vintage (school year 1999-2000) and Census 2010 vintage (2009-2010)
    for suf, sub in (("00", "2000"), ("10", "2010")):
        for lay in LAYERS:
            for s in STATES:
                f = f"tl_2010_{s}_{lay}{suf}.zip"
                out.append((f"{T}/TIGER2010/{lay.upper()}/{sub}/{f}", RAW / "tiger" / f"v20{suf}c" / f))
    # 2008 and 2009: state folders
    for y in (2008, 2009):
        folders = state_folders(y)
        for lay in LAYERS:
            for s in STATES:
                f = f"tl_{y}_{s}_{lay}.zip"
                out.append((f"{T}/TIGER{y}/{folders[s]}/{f}", RAW / "tiger" / f"v{y}" / f))
    # 2011-2025: one folder per layer
    for y in range(2011, 2026):
        for lay in LAYERS:
            for s in STATES:
                f = f"tl_{y}_{s}_{lay}.zip"
                out.append((f"{T}/TIGER{y}/{lay.upper()}/{f}", RAW / "tiger" / f"v{y}" / f))
        if y >= 2022:
            for s in STATES:
                f = f"tl_{y}_{s}_sdadm.zip"
                out.append((f"{T}/TIGER{y}/SDADM/{f}", RAW / "tiger" / f"v{y}" / f))
    # Map geometry: 2024 and 2025 cartographic boundaries (national files)
    for y in (2024, 2025):
        for lay in LAYERS:
            f = f"cb_{y}_us_{lay}_500k.zip"
            out.append((f"{T}/GENZ{y}/shp/{f}", RAW / "cb" / f))
    return [(u, d) for u, d in out if d.exists() or u.rsplit("/", 1)[1] in listed(u.rsplit("/", 1)[0] + "/")]


def main():
    js = jobs()
    with ThreadPoolExecutor(4) as ex:
        res = list(ex.map(lambda j: (j, fetch(*j)), js))
    missing = [j[0][0].rsplit("/", 1)[1] for j in res if not j[1]]
    print(f"{len(js) - len(missing)} downloaded, {len(missing)} not on server (states without that layer)")
    (RAW / "tiger").mkdir(parents=True, exist_ok=True)
    (RAW / "tiger" / "missing.txt").write_text("\n".join(sorted(missing)))


if __name__ == "__main__":
    main()
