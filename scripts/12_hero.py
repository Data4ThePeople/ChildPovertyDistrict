"""Hero source image: the 2024 child poverty map rendered at hero scale (1680x1080) in the dark
house palette, with the title and the national figure beside it. `hero pad` then adds the padding.

Same data, bins, floor and color ramp as the viz's 2024 view (darker = more children in poverty, in
both light and dark mode; the deepest step clears 2:1 contrast on the dark background)."""
import json
import os

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.collections import PolyCollection  # noqa: E402

from common import PROC, ROOT  # noqa: E402

OUT = ROOT / "posts" / "children-poverty-viz" / "images" / "children-poverty-viz-hero-source.png"
BG, INK, MUTED = "#181A1B", "#BBBDC0", "#8C9094"
RAMP = ["#ffdacd", "#ffbaa3", "#fe9979", "#f37952", "#df5f35", "#c24d25", "#a33f1e"]   # viz --s0..--s6, same in light and dark mode
SMALL, EDGE, STATE = "#50565A", "#181A1B", "#9AA5A1"
BINS, FLOOR = [5, 10, 15, 20, 25, 30], 100


def rings(polys, outer_only=False):
    for poly in polys:
        for r in (poly[:1] if outer_only else poly):
            yield np.cumsum(np.array(r, dtype=float).reshape(-1, 2), axis=0)


def area(xy):
    x, y = xy[:, 0], xy[:, 1]
    return abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1))) / 2


def main():
    md = json.loads((PROC / "map_data.json").read_text())
    i24 = md["years"].index(2024)
    k = sum(d["k"][i24] for d in md["d"])
    p = sum(d["p"][i24] for d in md["d"])
    rate = 100 * p / k
    assert round(rate, 1) == 14.4, rate   # matches the tie-out

    polys, cols = [], []
    for d in md["d"]:
        if d["l"] == "s":           # secondary districts overlap elementary ones; the viz does not fill them
            continue
        kk, pp = d["k"][i24], d["p"][i24]
        col = SMALL if kk < FLOOR else RAMP[int(np.searchsorted(BINS, 100 * pp / kk, side="right"))]
        for r in rings(md["geo"][d["id"]], outer_only=True):   # outer rings, largest first, so enclaves sit on top
            polys.append(r)
            cols.append(col)
    order = np.argsort([-area(r) for r in polys])
    polys, cols = [polys[i] for i in order], [cols[i] for i in order]
    borders = [r for b in md["borders"] for r in rings(b)]
    allxy = np.vstack(polys)
    x0, y0 = allxy.min(0)
    x1, y1 = allxy.max(0)

    plt.rcParams.update({"text.parse_math": False, "font.family": "DejaVu Sans"})
    fig = plt.figure(figsize=(16.8, 10.8), dpi=100, facecolor=BG)
    ax = fig.add_axes([0.01, 0.17, 0.63, 0.74], facecolor=BG)
    ax.set_anchor("N")
    ax.add_collection(PolyCollection(polys, facecolors=cols, edgecolors=cols, linewidths=0.15))
    ax.add_collection(PolyCollection(borders, facecolors="none", edgecolors=STATE, linewidths=0.6))
    ax.set_xlim(x0, x1)
    ax.set_ylim(y1, y0)            # grid y points down
    ax.set_aspect("equal")
    ax.axis("off")
    fig.text(0.03, 0.94, "Child poverty rate, ages 5 to 17, by school district, 2024", fontsize=28, fontweight="bold", color=INK)

    # legend strip under the map
    lx, ly, lw, lh = 0.10, 0.105, 0.42, 0.028
    for i, c in enumerate(RAMP):
        fig.patches.append(plt.Rectangle((lx + i * lw / 7, ly), lw / 7, lh, transform=fig.transFigure, color=c, figure=fig))
    for i, b in enumerate(BINS):
        fig.text(lx + (i + 1) * lw / 7, ly - 0.012, f"{b}%", fontsize=17, color=INK, ha="center", va="top")
    fig.text(lx, ly + lh + 0.012, "Darker = more children in poverty", fontsize=16, color=MUTED, va="bottom")
    fig.patches.append(plt.Rectangle((lx + lw + 0.02, ly), 0.022, lh, transform=fig.transFigure, color=SMALL, figure=fig))
    fig.text(lx + lw + 0.047, ly + lh / 2, "Fewer than\n100 children", fontsize=14, color=MUTED, va="center", linespacing=1.1)

    tx = 0.66
    fig.text(tx, 0.80, "Child Poverty\nby School\nDistrict", fontsize=50, fontweight="bold", color=INK, va="top", linespacing=1.05)
    fig.text(tx, 0.47, f"{rate:.1f}%", fontsize=72, fontweight="bold", color=RAMP[4], va="top")
    fig.text(tx, 0.345, "of school-age children lived\nin families in poverty in 2024", fontsize=22, color=INK, va="top", linespacing=1.25)
    fig.text(tx, 0.225, "Every U.S. school district\n2005 to 2024", fontsize=18, color=MUTED, va="top", linespacing=1.35)
    fig.text(tx, 0.075, "Data 4 The People  ·  Source: U.S. Census Bureau, SAIPE", fontsize=14, color=MUTED)
    os.makedirs(OUT.parent, exist_ok=True)
    fig.savefig(OUT, facecolor=BG)
    print("wrote", OUT, f"2024 rate {rate:.1f}%")


if __name__ == "__main__":
    main()
