"""Match each SAIPE year to the TIGER boundary vintage it was estimated on.

For every (SAIPE year, vintage) pair we count district IDs in SAIPE but not in the
vintage ("missing") and IDs in the vintage but not in SAIPE ("extra"), leaving out
Vermont (reported by supervisory union) and TIGER placeholder codes (LEA 999xx).
The vintage with the fewest differences (missing + extra) is the match. A match with more than
EXACT_MAX missing IDs is "approximate": the school year SAIPE used has no TIGER file.
An approximate year must also pass the crosswalk at its flank vintage, the exact
vintage of the next later SAIPE year that has one."""
import pandas as pd

from common import PROC, STATES
from common_geo import VINTAGES, read_layer, zip_path

YEARS = list(range(1999, 2025))
EXACT_MAX = 5


def vintage_ids():
    ids = {}
    for vkey, ytag, suf in VINTAGES:
        s = set()
        for st in STATES:
            for layer in ("unsd", "elsd", "scsd"):
                p = zip_path(vkey, ytag, suf, st, layer)
                if p.exists():
                    s |= set(read_layer(p, geometry=False).geoid)
        ids[vkey] = {g for g in s if not g[2:].startswith("999") and g[:2] != "50"}
    return ids


def main():
    saipe = pd.read_csv(PROC / "saipe_all_years.csv", dtype={"geoid": str})
    ids = vintage_ids()
    order = [v for v, _, _ in VINTAGES]
    rows, diffs = [], []
    for y in YEARS:
        S = {g for g in saipe.geoid[saipe.year == y] if g[:2] != "50"}
        sc = {v: (len(S - ids[v]), len(ids[v] - S)) for v in order}
        diffs.append({"year": y, **{v: f"{m}/{e}" for v, (m, e) in sc.items()}})
        # fewest total differences, then fewest missing, then latest vintage (identical files repeat)
        best = min(order, key=lambda v: (sc[v][0] + sc[v][1], sc[v][0], -order.index(v)))
        rows.append({"year": y, "vintage": best, "missing": sc[best][0], "extra": sc[best][1],
                     "exact": sc[best][0] <= EXACT_MAX})
    m = pd.DataFrame(rows)
    flank = []
    for i, r in enumerate(m.itertuples()):
        if r.exact:
            flank.append("")
            continue
        f = m[(m.year > r.year) & m.exact].iloc[0].vintage
        flank.append(f)
        if r.vintage == f:  # test vintage must differ from the flank, or the flank check means nothing
            sc = {v: tuple(int(x) for x in diffs[i][v].split("/")) for v in order if v != f}
            best = min(sc, key=lambda v: (sc[v][0] + sc[v][1], sc[v][0], -order.index(v)))
            m.loc[i, ["vintage", "missing", "extra"]] = [best, sc[best][0], sc[best][1]]
    m["flank"] = flank
    m.to_csv(PROC / "saipe_vintage_match_final.csv", index=False)
    pd.DataFrame(diffs).to_csv(PROC / "saipe_vintage_id_diffs.csv", index=False)
    print(m.to_string(index=False))


if __name__ == "__main__":
    main()
