"""Shared paths, HTTP helper and state list for the pipeline."""
import os
import threading
import time
import zipfile
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
PROC = ROOT / "data" / "processed"
UA = "Mozilla/5.0 (Macintosh) Data4ThePeople research eric@asaltollc.com"

# 50 states + DC (territories dropped)
STATES = ["01", "02", "04", "05", "06", "08", "09", "10", "11", "12", "13", "15", "16", "17",
          "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31",
          "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "44", "45", "46",
          "47", "48", "49", "50", "51", "53", "54", "55", "56"]

# SAIPE years used in the map (see DATASETS.md, method eras)
MAP_YEARS = list(range(2005, 2025))
ALL_SAIPE_YEARS = [1995, 1997] + list(range(1999, 2025))


def fetch(url, dest, tries=8):
    """Download url to dest unless it already exists. Returns False on 404."""
    dest = Path(dest)
    if dest.exists() and dest.stat().st_size > 0:
        return True
    dest.parent.mkdir(parents=True, exist_ok=True)
    for i in range(tries):
        try:
            r = requests.get(url, headers={"User-Agent": UA}, timeout=(20, 120), stream=True)
            if r.status_code == 404:
                return False
            if r.status_code in (429, 503):
                print(f"{r.status_code} on {url.rsplit('/', 1)[1]}, retry {i + 1}", flush=True)
                time.sleep(5 * (i + 1))
                continue
            r.raise_for_status()
            tmp = dest.with_suffix(dest.suffix + f".{os.getpid()}.{threading.get_ident()}.part")
            with open(tmp, "wb") as f:
                for chunk in r.iter_content(1 << 20):
                    f.write(chunk)
            if dest.suffix == ".zip" and not zipfile.is_zipfile(tmp):
                tmp.unlink()
                print(f"not a zip: {url.rsplit('/', 1)[1]}, retry {i + 1}", flush=True)
                time.sleep(5 * (i + 1))
                continue
            os.replace(tmp, dest)
            return True
        except requests.RequestException:
            if i == tries - 1:
                raise
            time.sleep(2 ** i)
    # The www2 firewall rejects a few files outright (e.g. tl_2017_34_unsd.zip); the FTP mirror serves them.
    if url.startswith("https://www2.census.gov/"):
        import urllib.request
        ftp = url.replace("https://www2.census.gov/", "ftp://ftp2.census.gov/")
        urllib.request.urlretrieve(ftp, dest)
        if zipfile.is_zipfile(dest):
            return True
        dest.unlink()
    raise RuntimeError(f"gave up on {url}")
