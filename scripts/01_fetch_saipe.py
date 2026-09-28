"""Download SAIPE national school district files, 1995-2024, and parse them to one CSV."""
import csv

from common import ALL_SAIPE_YEARS, PROC, RAW, fetch

BASE = "https://www2.census.gov/programs-surveys/saipe/datasets"


def fname(y):
    yy = f"{y % 100:02d}"
    return f"ussd{yy}.dat" if y <= 2002 else f"ussd{yy}.txt"


def parse(path):
    rows = {}
    for line in open(path, encoding="latin-1"):
        t = line.split()
        if len(t) < 7:
            continue
        i = next(k for k, x in enumerate(t) if x.lower().startswith("ussd"))
        geoid = t[0].zfill(2) + t[1].zfill(5)
        if geoid in rows:
            raise ValueError(f"duplicate {geoid} in {path}")
        rows[geoid] = (" ".join(t[2:i - 3]), int(t[i - 3]), int(t[i - 2]), int(t[i - 1]))
    return rows


def main():
    out = []
    for y in ALL_SAIPE_YEARS:
        f = fname(y)
        dest = RAW / "saipe" / f
        if not fetch(f"{BASE}/{y}/{y}-school-districts/{f}", dest):
            raise SystemExit(f"missing {f}")
        rows = parse(dest)
        kids = sum(r[2] for r in rows.values())
        pov = sum(r[3] for r in rows.values())
        print(f"{y}: {len(rows):,} districts, {kids:,} kids 5-17, {pov:,} in poverty, {100 * pov / kids:.1f}%")
        out += [(y, g, *r) for g, r in rows.items()]
    PROC.mkdir(parents=True, exist_ok=True)
    with open(PROC / "saipe_all_years.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["year", "geoid", "name", "pop_total", "kids_5_17", "kids_pov"])
        w.writerows(out)


if __name__ == "__main__":
    main()
