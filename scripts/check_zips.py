"""Delete any zip under data/raw that fails an integrity test, so a re-run fetches it again."""
import zipfile

from common import RAW

bad = []
for p in sorted(RAW.rglob("*.zip")):
    try:
        with zipfile.ZipFile(p) as z:
            if z.testzip() is not None:
                raise zipfile.BadZipFile
    except zipfile.BadZipFile:
        bad.append(p)
        p.unlink()
print(f"{len(bad)} bad zips removed", *[b.name for b in bad])
