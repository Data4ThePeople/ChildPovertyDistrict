"""Stitch each 2024 district's history onto its 2024 geography.

For a 2024 district D and a SAIPE year Y estimated on boundary vintage V:
  - a V district C is a component of D when >= PURITY of C's children (2020 blocks) live in D
  - D passes when its components hold >= COVER of D's children
  - unified D may be built from old elementary districts; then the old secondary
    districts over that area must also be components (their counts are for the
    high-school grade span, so elementary + secondary = the unified total)
  - elementary and secondary D only take components from the same layer
  - D's value for Y is the sum of its components' SAIPE counts (exact; nothing is interpolated)
Years whose boundary school year has no TIGER file ("approx") must also pass at the next
exact vintage with the same component set. History runs back from 2024 and stops at the
first year that fails."""
import glob
import json

import pandas as pd

from common import MAP_YEARS, PROC, RAW

PURITY = 0.95
COVER = 0.95
# Component layer groups tried in order. Vermont supervisory unions (sdadm) match their own
# layer where it exists (2022 on), otherwise the member districts that make them up.
BASE_GROUPS = {"unsd": [("unsd", "elsd")], "elsd": [("elsd",)], "scsd": [("scsd",)],
               "sdadm": [("sdadm",), ("unsd", "elsd")]}


def load_match():
    m = pd.read_csv(PROC / "saipe_vintage_match_final.csv")
    return {r.year: (r.vintage, r.exact, r.flank) for r in m.itertuples()}


def components(asg, tcol, vcol_by_layer, base_layers, k12_target):
    """Return {target geoid: (sorted component list, coverage, min purity)} for passing targets."""
    have = asg[asg[tcol] > 0]
    kidsD = have.groupby(tcol).kids.sum()
    base_parts = []
    for lay in base_layers:
        vcol = vcol_by_layer.get(lay)
        if vcol is None:
            continue
        tot = asg[asg[vcol] > 0].groupby(vcol).kids.sum()
        h = have[have[vcol] > 0]
        ins = (pd.DataFrame({tcol: h[tcol].values, "c": h[vcol].values, "kids": h.kids.values})
               .groupby([tcol, "c"]).kids.sum().rename("inside").reset_index())
        ins["purity"] = ins.inside / ins.c.map(tot)
        ins["layer"] = lay
        base_parts.append(ins)
    if not base_parts:
        return {}
    ins = pd.concat(base_parts)
    comp = ins[ins.purity >= PURITY]
    cov = comp.groupby(tcol).inside.sum() / kidsD
    ok = cov[cov >= COVER].index
    out = {}
    sec_needed = k12_target and "elsd" in base_layers and "scsd" in vcol_by_layer
    if sec_needed:
        scol, ecol = vcol_by_layer["scsd"], vcol_by_layer.get("elsd")
        stot = asg[asg[scol] > 0].groupby(scol).kids.sum()
    for d in ok:
        c = comp[comp[tcol] == d]
        parts = [(x.layer, int(x.c)) for x in c.itertuples()]
        minp = c.purity.min()
        if sec_needed and ecol and (c.layer == "elsd").any():
            elem_ids = set(c.c[c.layer == "elsd"])
            area = have[(have[tcol] == d) & have[ecol].isin(elem_ids)]
            s_in = area[area[scol] > 0].groupby(scol).kids.sum()
            s_pur = have[(have[tcol] == d) & (have[scol].isin(s_in.index))].groupby(scol).kids.sum() / stot
            s_ok = s_pur[s_pur >= PURITY].index
            if s_in[s_in.index.isin(s_ok)].sum() < COVER * area.kids.sum():
                continue
            parts += [("scsd", int(s)) for s in s_ok]
            minp = min(minp, s_pur[s_ok].min())
        out[d] = (sorted(parts), float(cov[d]), float(minp))
    return out


def main():
    match = load_match()
    saipe = pd.read_csv(PROC / "saipe_all_years.csv", dtype={"geoid": str})
    sy = {y: g.set_index("geoid")[["kids_5_17", "kids_pov"]] for y, g in saipe.groupby("year")}
    tv = match[2024][0]
    asg = pd.concat([pd.read_parquet(f) for f in sorted(glob.glob(str(RAW / "assign" / "*.parquet")))],
                    ignore_index=True)
    vcols_all = [c for c in asg.columns if c.startswith("v")]
    asg[vcols_all] = asg[vcols_all].fillna(0).astype("int64")
    years = sorted(MAP_YEARS, reverse=True)
    rows, xw = [], []
    done = set()  # a geoid is a target in one layer only (sdadm last, so it only adds Vermont unions)
    for tlayer in ("unsd", "elsd", "scsd", "sdadm"):
        tcol = f"{tv}_{tlayer}"
        if tcol not in asg:
            continue
        # only 2024 SAIPE districts are targets
        targets = {int(g) for g in sy[2024].index} & set(asg[tcol].unique()) - done
        done |= targets
        alive = set(targets)
        cache = {}

        def comps_for(v, grp):
            if (v, grp) not in cache:
                vcols = {lay: f"{v}_{lay}" for lay in grp + ("scsd",) if f"{v}_{lay}" in asg}
                cache[v, grp] = components(asg, tcol, vcols, grp, tlayer in ("unsd", "sdadm"))
            return cache[v, grp]

        def attempt(d, y, v, exact, flank, grp):
            r = comps_for(v, grp).get(d)
            if r is None:
                return None
            if not exact:
                f = comps_for(flank, grp).get(d)
                if f is None or f[0] != r[0]:
                    return None
            ids = [f"{c:07d}" for _, c in r[0]]
            return (r, ids) if all(i in sy[y].index for i in ids) else None

        for y in years:
            v, exact, flank = match[y]
            for d in sorted(alive):
                hit = next((a for g in BASE_GROUPS[tlayer] if (a := attempt(d, y, v, exact, flank, g))), None)
                if hit is None:
                    alive.discard(d)
                    continue
                r, ids = hit
                k = int(sy[y].loc[ids, "kids_5_17"].sum())
                p = int(sy[y].loc[ids, "kids_pov"].sum())
                gid = f"{d:07d}"
                kind = "same" if ids == [gid] and r[0][0][0] == tlayer else "merge"
                rows.append((gid, tlayer, y, k, p))
                xw.append((gid, tlayer, y, v, kind, ";".join(f"{l}:{i}" for (l, _), i in zip(r[0], ids)),
                           round(r[1], 4), round(r[2], 4)))
        print(f"{tlayer}: {len(targets):,} targets; with 2000 history: {len(alive):,}", flush=True)
    pd.DataFrame(rows, columns=["geoid", "layer", "year", "kids_5_17", "kids_pov"]).to_csv(
        PROC / "district_series.csv", index=False)
    pd.DataFrame(xw, columns=["geoid", "layer", "year", "vintage", "kind", "components", "coverage",
                              "min_purity"]).to_csv(PROC / "crosswalk.csv", index=False)


if __name__ == "__main__":
    main()
