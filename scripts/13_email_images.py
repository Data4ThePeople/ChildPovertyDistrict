"""Email images for the Mailchimp teaser (step 2g):
  - 02-viz-screenshot-email.jpg: a picture of the live tool (embed view, 2x capture scaled to 1200x780)
  - children-poverty-viz-hero-email.jpg: the hero as a JPG under 300 KB
change_map() is kept but no longer used in the email (Eric: the email opens on 2025 Census figures).
Same rules as the viz: pooled three-year rates, 100+ children a year in both periods to shade,
the viz's dark-mode diverging colors (blue = fewer children in poverty)."""
import json

import matplotlib
import numpy as np
from PIL import Image

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.collections import PolyCollection  # noqa: E402

from common import PROC, ROOT  # noqa: E402

IMG = ROOT / "posts" / "children-poverty-viz" / "images"
BG, INK, MUTED = "#181A1B", "#BBBDC0", "#8C9094"
DIV = ["#1c5cab", "#5598e7", "#b7d3f6", "#383835", "#f6b8a8", "#e0604c", "#a52a24"]   # viz --dn3..--up3 (dark-mode neutral)
LABELS = ["−10", "−5", "−2", "+2", "+5", "+10"]
BINS = [-10, -5, -2, 2, 5, 10]
SMALL, NOHIST, STATE = "#6B7175", "#181A1B", "#9AA5A1"   # no comparable figure = left blank
W0, W1 = [2005, 2006, 2007], [2022, 2023, 2024]


def rings(polys):
    for poly in polys:
        yield np.cumsum(np.array(poly[0], dtype=float).reshape(-1, 2), axis=0)


def area(xy):
    x, y = xy[:, 0], xy[:, 1]
    return abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1))) / 2


def change_map():
    md = json.loads((PROC / "map_data.json").read_text())
    yi = {y: i for i, y in enumerate(md["years"])}
    polys, cols, n, down, up = [], [], 0, 0, 0
    for d in md["d"]:
        if d["l"] == "s":
            continue
        ks = [d["k"][yi[y]] for y in W0 + W1]
        if any(v is None for v in ks):
            col = NOHIST
        else:
            k0, k1 = sum(ks[:3]), sum(ks[3:])
            p0, p1 = sum(d["p"][yi[y]] for y in W0), sum(d["p"][yi[y]] for y in W1)
            if k0 / 3 < 100 or k1 / 3 < 100:
                col = SMALL
            else:
                v = 100 * p1 / k1 - 100 * p0 / k0
                col = DIV[int(np.searchsorted(BINS, v, side="right"))]
        for r in rings(md["geo"][d["id"]]):
            polys.append(r)
            cols.append(col)
    order = np.argsort([-area(r) for r in polys])
    polys, cols = [polys[i] for i in order], [cols[i] for i in order]
    borders = [np.cumsum(np.array(r, dtype=float).reshape(-1, 2), axis=0) for b in md["borders"] for p in b for r in p]
    allxy = np.vstack(polys)
    (x0, y0), (x1, y1) = allxy.min(0), allxy.max(0)

    plt.rcParams.update({"text.parse_math": False, "font.family": "DejaVu Sans"})
    fig = plt.figure(figsize=(12, 9), dpi=100, facecolor=BG)
    fig.text(0.04, 0.95, "Change in child poverty rate by school district", fontsize=24, fontweight="bold", color=INK, va="top")
    fig.text(0.04, 0.905, "Pooled rate, 2005-2007 to 2022-2024, percentage points. Blue = fewer children in poverty.",
             fontsize=14, color=MUTED, va="top")
    ax = fig.add_axes([0.02, 0.17, 0.96, 0.70], facecolor=BG)
    ax.set_anchor("N")
    ax.add_collection(PolyCollection(polys, facecolors=cols, edgecolors=cols, linewidths=0.15))
    ax.add_collection(PolyCollection(borders, facecolors="none", edgecolors=STATE, linewidths=0.5))
    ax.set_xlim(x0, x1)
    ax.set_ylim(y1, y0)
    ax.set_aspect("equal")
    ax.axis("off")
    lx, ly, lw, lh = 0.20, 0.085, 0.42, 0.03
    for i, c in enumerate(DIV):
        fig.patches.append(plt.Rectangle((lx + i * lw / 7, ly), lw / 7, lh, transform=fig.transFigure, color=c, figure=fig))
    for i, t in enumerate(LABELS):
        fig.text(lx + (i + 1) * lw / 7, ly - 0.012, t, fontsize=13, color=INK, ha="center", va="top")
    fig.text(lx + 3.5 * lw / 7, ly + lh + 0.008, "within 2", fontsize=12, color=MUTED, ha="center", va="bottom")
    for j, (c, t) in enumerate([(SMALL, "Fewer than 100 children"), (NOHIST, "Blank: no comparable figure")]):
        y = ly + lh - j * 0.035
        fig.patches.append(plt.Rectangle((lx + lw + 0.03, y - 0.022), 0.022, 0.022, transform=fig.transFigure, facecolor=c,
                                         edgecolor=MUTED, linewidth=0.8, figure=fig))
        fig.text(lx + lw + 0.058, y - 0.011, t, fontsize=12, color=MUTED, va="center")
    fig.text(0.04, 0.025, "Data 4 The People  ·  Source: U.S. Census Bureau, SAIPE school district estimates", fontsize=11, color=MUTED)
    out = IMG / "01-change-map-email.png"
    fig.savefig(out, facecolor=BG)
    jpg = out.with_suffix(".jpg")
    Image.open(out).convert("RGB").save(jpg, "JPEG", quality=88, optimize=True, progressive=True)
    print("wrote", out, "and", jpg, f"{jpg.stat().st_size / 1000:.0f} KB")
    assert jpg.stat().st_size < 300_000


def hero_jpg():
    src = IMG / "children-poverty-viz-hero-1680x1080.png"
    out = IMG / "children-poverty-viz-hero-email.jpg"
    im = Image.open(src).convert("RGB")
    for q in (88, 82, 76, 70, 64):
        im.save(out, "JPEG", quality=q, optimize=True, progressive=True)
        if out.stat().st_size < 300_000:
            break
    print("wrote", out, f"{out.stat().st_size / 1000:.0f} KB, quality {q}")
    assert out.stat().st_size < 300_000


def viz_screenshot():
    import subprocess
    import tempfile
    chrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    out = IMG / "02-viz-screenshot-email.jpg"
    with tempfile.TemporaryDirectory() as d:
        png = f"{d}/viz.png"
        subprocess.run([chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=2",
                        "--virtual-time-budget=15000", "--window-size=1200,780", f"--screenshot={png}",
                        f"file://{ROOT / 'dist' / 'index.html'}#embed=1"], capture_output=True, timeout=300)
        im = Image.open(png).convert("RGB").resize((1200, 780), Image.LANCZOS)
    for q in (90, 85, 80, 75):
        im.save(out, "JPEG", quality=q, optimize=True, progressive=True)
        if out.stat().st_size < 300_000:
            break
    print("wrote", out, f"{out.stat().st_size / 1000:.0f} KB, quality {q}")
    assert out.stat().st_size < 300_000


if __name__ == "__main__":
    viz_screenshot()
    hero_jpg()
