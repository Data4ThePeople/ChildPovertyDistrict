"use strict";
// Child poverty by school district. Vanilla JS on canvas; every number is computed here from DATA.
(async function () {
  const root = document.getElementById("cp");
  let framed = false;
  try { framed = window.self !== window.top; } catch (e) { framed = true; }
  const hashFlags = new URLSearchParams(location.hash.slice(1));
  if (hashFlags.get("embed") === "1") framed = true;
  if (framed) { root.classList.add("framed"); document.documentElement.setAttribute("data-theme", "light"); }

  const $ = (id) => document.getElementById(id);
  const MAP_FLOOR = 100, RANK_FLOOR = 500, TOP_N = 25;
  const RATE_BINS = [5, 10, 15, 20, 25, 30];                  // percent; 7 classes
  const RATE_LABELS = ["Under 5%", "5% to 10%", "10% to 15%", "15% to 20%", "20% to 25%", "25% to 30%", "30% or more"];
  const CHG_BINS = [-10, -5, -2, 2, 5, 10];                    // percentage points; 7 classes
  const CHG_LABELS = ["Down 10 points or more", "Down 5 to 10", "Down 2 to 5", "Within 2 points", "Up 2 to 5", "Up 5 to 10", "Up 10 points or more"];
  const CHG_VARS = ["--dn3", "--dn2", "--dn1", "--mid", "--up1", "--up2", "--up3"];
  const RATE_VARS = ["--s0", "--s1", "--s2", "--s3", "--s4", "--s5", "--s6"];
  const ACS_BINS = [15, 25, 35, 45, 55, 65];                   // percent below 200% of poverty; 7 classes
  const ACS_VARS = ["--a0", "--a1", "--a2", "--a3", "--a4", "--a5", "--a6"];
  const LAYER_NAME = { u: "Unified district", e: "Elementary district", s: "Secondary district", v: "Supervisory union (Vermont)" };

  // ---------- data ----------
  async function loadData() {
    const bin = Uint8Array.from(atob(DATA_B64), (c) => c.charCodeAt(0));
    const stream = new Blob([bin]).stream().pipeThrough(new DecompressionStream("gzip"));
    return JSON.parse(await new Response(stream).text());
  }
  const DATA = await loadData();
  const YEARS = DATA.years, NY = YEARS.length, GRID = DATA.grid, ACS = DATA.acs;
  const D = DATA.d;
  const byId = new Map();
  for (const d of D) {
    if (byId.has(d.id)) throw new Error("duplicate district id " + d.id);
    byId.set(d.id, d);
    d.first = d.k.findIndex((v) => v !== null);
  }

  // ---------- geometry ----------
  function decodeRing(a) {
    const out = new Float64Array(a.length);
    let x = 0, y = 0;
    for (let i = 0; i < a.length; i += 2) { x += a[i]; y += a[i + 1]; out[i] = x; out[i + 1] = y; }
    return out;
  }
  let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
  function buildPath(polys, bb) {
    const p = new Path2D();
    for (const rings of polys) for (const r of rings) {
      const c = decodeRing(r);
      p.moveTo(c[0], c[1]);
      for (let i = 2; i < c.length; i += 2) {
        p.lineTo(c[i], c[i + 1]);
        if (bb) {
          if (c[i] < bb[0]) bb[0] = c[i]; if (c[i] > bb[2]) bb[2] = c[i];
          if (c[i + 1] < bb[1]) bb[1] = c[i + 1]; if (c[i + 1] > bb[3]) bb[3] = c[i + 1];
        }
      }
      if (bb) {
        if (c[0] < bb[0]) bb[0] = c[0]; if (c[0] > bb[2]) bb[2] = c[0];
        if (c[1] < bb[1]) bb[1] = c[1]; if (c[1] > bb[3]) bb[3] = c[1];
      }
      p.closePath();
    }
    return p;
  }
  const fillList = [], secList = [];
  for (const d of D) {
    const g = DATA.geo[d.id];
    if (!g) continue;
    d.bb = [Infinity, Infinity, -Infinity, -Infinity];
    d.path = buildPath(g, d.bb);
    (d.l === "s" ? secList : fillList).push(d);
    if (d.l !== "s") {
      minX = Math.min(minX, d.bb[0]); minY = Math.min(minY, d.bb[1]);
      maxX = Math.max(maxX, d.bb[2]); maxY = Math.max(maxY, d.bb[3]);
    }
  }
  const borders = DATA.borders.map((b) => buildPath(b, null));
  const stateBB = {};
  for (const d of fillList) {
    const b = stateBB[d.s] || (stateBB[d.s] = [Infinity, Infinity, -Infinity, -Infinity]);
    b[0] = Math.min(b[0], d.bb[0]); b[1] = Math.min(b[1], d.bb[1]); b[2] = Math.max(b[2], d.bb[2]); b[3] = Math.max(b[3], d.bb[3]);
  }
  // uniform grid index over fill districts for hit testing
  const GX = 80, GY = 50, cellW = (maxX - minX) / GX, cellH = (maxY - minY) / GY;
  const cells = Array.from({ length: GX * GY }, () => []);
  for (const d of fillList) {
    const x0 = Math.max(0, Math.floor((d.bb[0] - minX) / cellW)), x1 = Math.min(GX - 1, Math.floor((d.bb[2] - minX) / cellW));
    const y0 = Math.max(0, Math.floor((d.bb[1] - minY) / cellH)), y1 = Math.min(GY - 1, Math.floor((d.bb[3] - minY) / cellH));
    for (let y = y0; y <= y1; y++) for (let x = x0; x <= x1; x++) cells[y * GX + x].push(d);
  }
  const hitCtx = document.createElement("canvas").getContext("2d");
  function hitTest(gx, gy) {
    const cx = Math.floor((gx - minX) / cellW), cy = Math.floor((gy - minY) / cellH);
    if (cx < 0 || cy < 0 || cx >= GX || cy >= GY) return null;
    for (const d of cells[cy * GX + cx]) {
      if (gx < d.bb[0] || gx > d.bb[2] || gy < d.bb[1] || gy > d.bb[3]) continue;
      if (hitCtx.isPointInPath(d.path, gx, gy, "evenodd")) return d;
    }
    return null;
  }

  // ---------- state ----------
  const S = { mode: "year", yi: NY - 1, from: null, to: null, st: "", sel: null, hover: null, rankTab: 0 };
  // change windows: every 3-year window of consecutive map years
  const WINDOWS = [];
  for (let i = 2; i < NY; i++) {
    if (YEARS[i] - YEARS[i - 2] === 2) WINDOWS.push({ label: `${YEARS[i] - 2}-${YEARS[i]}`, idx: [i - 2, i - 1, i] });
  }
  const defaultFrom = WINDOWS.findIndex((w) => w.label === "2005-2007");
  const defaultTo = WINDOWS.length - 1;
  S.from = defaultFrom; S.to = defaultTo;

  function pooled(d, w) {
    let k = 0, p = 0;
    for (const i of w.idx) { if (d.k[i] === null) return null; k += d.k[i]; p += d.p[i]; }
    return k > 0 ? { k, p, rate: (100 * p) / k, avgK: k / w.idx.length } : null;
  }
  // value of a district in the current view: {v, cls, k, p} or {cls:"small"|"nohist"}
  function acsVal(d) {
    if (!d.a) return { cls: "nohist" };
    const [r10, m10, k, b, shade] = d.a, v = r10 / 10, moe = m10 / 10;
    if (!shade) return { cls: "small", v, moe, k, b };  // too few children or margin of error too wide (decided in the build)
    return { v, moe, k, b, cls: binOf(v, ACS_BINS) };
  }
  function value(d) {
    if (S.mode === "acs") return acsVal(d);
    if (S.mode === "year") {
      const k = d.k[S.yi], p = d.p[S.yi];
      if (k === null) return { cls: "nohist" };
      if (k < MAP_FLOOR || k === 0) return { cls: "small", k, p };
      const v = (100 * p) / k;
      return { v, cls: binOf(v, RATE_BINS), k, p };
    }
    const a = pooled(d, WINDOWS[S.from]), b = pooled(d, WINDOWS[S.to]);
    if (!a || !b) return { cls: "nohist" };
    if (a.avgK < MAP_FLOOR || b.avgK < MAP_FLOOR) return { cls: "small", a, b };
    const v = b.rate - a.rate;
    return { v, cls: binOf(v, CHG_BINS), a, b };
  }
  function binOf(v, bins) { let i = 0; while (i < bins.length && v >= bins[i]) i++; return i; }

  // ---------- colors ----------
  let C = {};
  function readColors() {
    const cs = getComputedStyle(root);
    const g = (n) => cs.getPropertyValue(n).trim();
    C = { rate: RATE_VARS.map(g), chg: CHG_VARS.map(g), acs: ACS_VARS.map(g), small: g("--small"), unc: g("--unc"), nohist: g("--nohist"), hatch: g("--hatch"),
      edge: g("--edge"), state: g("--state"), hi: g("--hi"), panel: g("--panel"), ink3: g("--ink-3"), accent: g("--accent") };
    const pc = document.createElement("canvas"); pc.width = pc.height = 8;
    const x = pc.getContext("2d");
    x.fillStyle = C.nohist; x.fillRect(0, 0, 8, 8);
    x.strokeStyle = C.hatch; x.lineWidth = 1.2; x.beginPath(); x.moveTo(-2, 10); x.lineTo(10, -2); x.moveTo(-2, 2); x.lineTo(2, -2); x.moveTo(6, 10); x.lineTo(10, 6); x.stroke();
    C.hatchPat = bctx.createPattern(pc, "repeat");
  }
  function colorOf(val) {
    if (val.cls === "nohist") return C.hatchPat;
    if (val.cls === "small") return S.mode === "acs" ? C.unc : C.small;
    return S.mode === "year" ? C.rate[val.cls] : S.mode === "acs" ? C.acs[val.cls] : C.chg[val.cls];
  }

  // ---------- canvas & view ----------
  const cv = $("map"), wrap = $("mapbox");
  const ctx = cv.getContext("2d");
  let W = 0, H = 0, dpr = 1;
  const view = { k: 1, tx: 0, ty: 0 };
  function fitBox(bb, pad = 0.06, maxK = Infinity) {
    const bw = bb[2] - bb[0], bh = bb[3] - bb[1];
    const k = Math.min(maxK, Math.min(W * (1 - 2 * pad) / bw, H * (1 - 2 * pad) / bh));
    view.k = k; view.tx = (W - bw * k) / 2 - bb[0] * k; view.ty = (H - bh * k) / 2 - bb[1] * k;
  }
  let homeK = 1, pendingSel = null;
  function home() {
    if (S.st && stateBB[S.st]) fitBox(stateBB[S.st]); else fitBox([minX, minY, maxX, maxY], 0.03);
    if (!S.st) homeK = view.k;
  }
  function resize() {
    const r = wrap.getBoundingClientRect();
    const first = W === 0;
    dpr = Math.min(2, window.devicePixelRatio || 1);
    W = r.width; H = r.height;
    cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr);
    if (first) {
      fitBox([minX, minY, maxX, maxY], 0.03); homeK = view.k; home();
      if (pendingSel) { select(pendingSel, true); pendingSel = null; return; }
    }
    draw();
  }

  let vals = new Map();
  function computeVals() { vals = new Map(); for (const d of D) vals.set(d.id, value(d)); }

  // Two layers: the district fills are rendered once into an offscreen "base" bitmap at a known view;
  // hover and selection outlines are drawn on top of a copy of it, so moving the mouse never repaints
  // 13,000 districts. While panning or zooming, the base bitmap is moved and scaled, and a sharp
  // re-render happens once the gesture settles.
  const base = document.createElement("canvas"), bctx = base.getContext("2d");
  let frame = 0, baseDirty = true, baseView = null, settleT = 0;
  function schedule() { if (!W) return; cancelAnimationFrame(frame); frame = requestAnimationFrame(render); }
  function draw() { baseDirty = true; schedule(); }          // data, colors or size changed
  function drawOverlay() { schedule(); }                      // only hover / selection changed
  function interact() {                                       // view moving: reuse the bitmap now, re-render when it settles
    if (!baseView) baseDirty = true;
    schedule(); clearTimeout(settleT); settleT = setTimeout(draw, 160);
  }
  function render() {
    if (baseDirty) { renderBase(); baseDirty = false; }
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.fillStyle = C.panel; ctx.fillRect(0, 0, cv.width, cv.height);
    const r = view.k / baseView.k;
    ctx.setTransform(r, 0, 0, r, dpr * (view.tx - baseView.tx * r), dpr * (view.ty - baseView.ty * r));
    ctx.drawImage(base, 0, 0);
    ctx.setTransform(dpr * view.k, 0, 0, dpr * view.k, dpr * view.tx, dpr * view.ty);
    const lw = 1 / view.k;
    ctx.lineJoin = "round";
    const outline = (d, w, color) => { if (!d || !d.path) return; ctx.strokeStyle = color; ctx.lineWidth = w * lw; ctx.stroke(d.path); };
    const focus = S.hover || S.sel;
    if (focus && focus.l === "e" && focus.hs) outline(byId.get(focus.hs), 1.6, C.ink3);
    if (S.sel) outline(S.sel, 2.4, C.hi);
    if (S.hover && S.hover !== S.sel) outline(S.hover, 1.6, C.hi);
  }
  function renderBase() {
    if (base.width !== cv.width || base.height !== cv.height) { base.width = cv.width; base.height = cv.height; }
    const c = bctx;
    c.setTransform(1, 0, 0, 1, 0, 0);
    c.fillStyle = C.panel; c.fillRect(0, 0, base.width, base.height);
    c.setTransform(dpr * view.k, 0, 0, dpr * view.k, dpr * view.tx, dpr * view.ty);
    const x0 = -view.tx / view.k, y0 = -view.ty / view.k, x1 = (W - view.tx) / view.k, y1 = (H - view.ty) / view.k;
    const lw = 1 / view.k;
    c.lineJoin = "round";
    c.strokeStyle = C.edge; c.lineWidth = 0.6 * lw;
    const dim = S.st;
    for (const d of fillList) {
      if (d.bb[2] < x0 || d.bb[0] > x1 || d.bb[3] < y0 || d.bb[1] > y1) continue;
      c.globalAlpha = dim && d.s !== dim ? 0.3 : 1;
      c.fillStyle = colorOf(vals.get(d.id));
      c.fill(d.path, "evenodd");
      if (view.k * GRID > 30) c.stroke(d.path); // district edges once zoomed in enough to see them
    }
    c.globalAlpha = 1;
    c.strokeStyle = C.state; c.lineWidth = 0.9 * lw;
    for (const b of borders) c.stroke(b);
    baseView = { k: view.k, tx: view.tx, ty: view.ty };
  }

  // pan & zoom
  function zoomAt(f, sx, sy) {
    const k = Math.max(homeK * 0.8, Math.min(homeK * 400, view.k * f));
    const gx = (sx - view.tx) / view.k, gy = (sy - view.ty) / view.k;
    view.k = k; view.tx = sx - gx * k; view.ty = sy - gy * k;
    interact();
  }
  cv.addEventListener("wheel", (e) => { e.preventDefault(); const r = cv.getBoundingClientRect(); zoomAt(Math.exp(-e.deltaY * 0.0015), e.clientX - r.left, e.clientY - r.top); }, { passive: false });
  $("zin").onclick = () => zoomAt(1.6, W / 2, H / 2);
  $("zout").onclick = () => zoomAt(1 / 1.6, W / 2, H / 2);
  const ptrs = new Map();
  let drag = null, moved = false, pinch = null;
  cv.addEventListener("pointerdown", (e) => {
    cv.setPointerCapture(e.pointerId); ptrs.set(e.pointerId, [e.clientX, e.clientY]);
    moved = false;
    if (ptrs.size === 1) drag = { x: e.clientX, y: e.clientY, tx: view.tx, ty: view.ty };
    if (ptrs.size === 2) { const [a, b] = [...ptrs.values()]; pinch = { d: Math.hypot(a[0] - b[0], a[1] - b[1]), k: view.k }; drag = null; }
  });
  cv.addEventListener("pointermove", (e) => {
    const r = cv.getBoundingClientRect();
    if (ptrs.has(e.pointerId)) ptrs.set(e.pointerId, [e.clientX, e.clientY]);
    if (pinch && ptrs.size === 2) {
      const [a, b] = [...ptrs.values()];
      const dd = Math.hypot(a[0] - b[0], a[1] - b[1]);
      zoomAt((pinch.k * dd / pinch.d) / view.k, (a[0] + b[0]) / 2 - r.left, (a[1] + b[1]) / 2 - r.top);
      moved = true; return;
    }
    if (drag) {
      const dx = e.clientX - drag.x, dy = e.clientY - drag.y;
      if (Math.abs(dx) + Math.abs(dy) > 3) { moved = true; cv.classList.add("drag"); }
      if (moved) { view.tx = drag.tx + dx; view.ty = drag.ty + dy; hideTip(); interact(); return; }
    }
    if (e.pointerType === "mouse") hoverAt(e.clientX - r.left, e.clientY - r.top);
  });
  const endPtr = (e) => {
    ptrs.delete(e.pointerId);
    if (ptrs.size < 2) pinch = null;
    if (ptrs.size === 0) {
      cv.classList.remove("drag");
      if (drag && !moved) {
        const r = cv.getBoundingClientRect();
        const d = pick(e.clientX - r.left, e.clientY - r.top);
        select(d, false);
        if (e.pointerType !== "mouse") { S.hover = d; showTip(d, e.clientX - r.left, e.clientY - r.top); }
      }
      drag = null;
    }
  };
  cv.addEventListener("pointerup", endPtr);
  cv.addEventListener("pointercancel", endPtr);
  cv.addEventListener("pointerleave", () => { if (!drag) { S.hover = null; hideTip(); showDetail(S.sel); drawOverlay(); } });

  let clearT = 0;
  function pick(sx, sy) { return hitTest((sx - view.tx) / view.k, (sy - view.ty) / view.k); }
  function hoverAt(sx, sy) {
    const d = pick(sx, sy);
    if (d !== S.hover) {
      S.hover = d; drawOverlay();
      clearTimeout(clearT);
      // crossing a border or a gap briefly hits nothing; only clear the panel if the pointer stays off a district
      if (d) showDetail(d); else clearT = setTimeout(() => { if (!S.hover) showDetail(S.sel); }, 250);
    }
    if (d) showTip(d, sx, sy); else hideTip();
  }

  // ---------- formatting ----------
  const nf = new Intl.NumberFormat("en-US");
  const pct = (v) => v.toFixed(1) + "%";
  const pts = (v) => (v > 0 ? "+" : v < 0 ? "−" : "") + Math.abs(v).toFixed(1) + " points";
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const stAbbr = (s) => DATA.states[s][0];
  function acsText(v) {
    if (v.cls === "nohist") return "No ACS figure: the district's boundaries changed between the 2024 and 2025 boundary files.";
    const line = `${nf.format(v.b)} of ${nf.format(v.k)} children ages 6 to 17 below twice the poverty line (ACS ${ACS.period}, margin of error \u00b1${v.moe.toFixed(1)} points)`;
    return v.cls === "small" ? `Too uncertain to shade: ${pct(v.v)}, ${line}.` : line + ".";
  }
  function valueText(d, v) {
    if (S.mode === "acs") return acsText(v);
    if (v.cls === "nohist") return S.mode === "year"
      ? `No comparable figure for ${YEARS[S.yi]}. The district's boundaries were different then.`
      : "No comparable figures for both periods. The district's boundaries changed in between.";
    if (S.mode === "year") {
      const line = `${nf.format(v.p)} of ${nf.format(v.k)} children ages 5 to 17 in poverty`;
      return v.cls === "small" ? `Fewer than ${MAP_FLOOR} children ages 5 to 17 (${line}); too few to shade.` : line;
    }
    const w0 = WINDOWS[S.from].label, w1 = WINDOWS[S.to].label;
    const line = `${w0}: ${pct(v.a.rate)}. ${w1}: ${pct(v.b.rate)}.`;
    return v.cls === "small" ? `Fewer than ${MAP_FLOOR} children a year in one of the periods; too few to shade. ${line}` : line;
  }

  // ---------- tooltip ----------
  const tip = $("tip");
  function showTip(d, sx, sy) {
    const v = vals.get(d.id);
    let head = "";
    if (v.cls !== "nohist" && v.cls !== "small") head = S.mode === "year" ? pct(v.v) : S.mode === "acs" ? `${pct(v.v)} \u00b1${v.moe.toFixed(1)}` : pts(v.v);
    tip.innerHTML = `<b>${esc(d.n)}, ${stAbbr(d.s)}</b>${head ? `<span class="v">${head}</span><br>` : ""}<span>${esc(valueText(d, v))}</span>`;
    tip.hidden = false;
    const tw = tip.offsetWidth, th = tip.offsetHeight;
    let x = sx + 14, y = sy + 14;
    if (x + tw > W - 6) x = sx - tw - 14;
    if (y + th > H - 6) y = sy - th - 14;
    tip.style.left = Math.max(4, x) + "px"; tip.style.top = Math.max(4, y) + "px";
  }
  function hideTip() { tip.hidden = true; }

  // ---------- detail card with history chart ----------
  function spark(d) {
    const pts2 = [];
    for (let i = 0; i < NY; i++) if (d.k[i] !== null && d.k[i] > 0) pts2.push([YEARS[i], (100 * d.p[i]) / d.k[i], i]);
    if (!pts2.length) return "";
    const w = 300, h = 92, l = 30, r = 16, t = 8, b = 18;
    const xs = (y) => l + ((y - YEARS[0]) / (YEARS[NY - 1] - YEARS[0])) * (w - l - r);
    const hiV = Math.max(10, Math.ceil(Math.max(...pts2.map((p) => p[1])) / 10) * 10);
    const ys = (v) => t + (1 - v / hiV) * (h - t - b);
    let path = "", prev = null;
    for (const p of pts2) {
      const gap = prev && p[0] - prev[0] > 1;
      path += `${!prev || gap ? "M" : "L"}${xs(p[0]).toFixed(1)},${ys(p[1]).toFixed(1)}`;
      prev = p;
    }
    const grid = [0, hiV / 2, hiV].map((v) => `<line x1="${l}" x2="${w - r}" y1="${ys(v)}" y2="${ys(v)}" stroke="var(--grid)"/><text x="${l - 4}" y="${ys(v) + 3.5}" text-anchor="end" font-size="10" fill="var(--ink-3)">${v}%</text>`).join("");
    const xl = [YEARS[0], 2010, 2015, 2020, YEARS[NY - 1]].map((y) => `<text x="${xs(y)}" y="${h - 4}" text-anchor="middle" font-size="10" fill="var(--ink-3)">${y}</text>`).join("");
    const cur = S.mode === "year" ? pts2.find((p) => p[2] === S.yi) : null;
    const dots = pts2.map((p) => `<circle cx="${xs(p[0]).toFixed(1)}" cy="${ys(p[1]).toFixed(1)}" r="${p === cur ? 4 : 2.2}" fill="var(--accent)"${p === cur ? ' stroke="var(--panel)" stroke-width="1.5"' : ""}/>`).join("");
    return `<svg class="spark" viewBox="0 0 ${w} ${h}" preserveAspectRatio="none" role="img" aria-label="Child poverty rate by year, ${esc(d.n)}">${grid}${xl}<path d="${path}" fill="none" stroke="var(--accent)" stroke-width="2" stroke-linejoin="round"/>${dots}</svg>`;
  }
  function acsLine(d) {
    const a = acsVal(d);
    if (a.cls === "nohist") return "Below twice the poverty line (ACS): no figure for this district.";
    return `Below twice the poverty line, ages 6 to 17 (ACS ${ACS.period}): ${pct(a.v)} \u00b1${a.moe.toFixed(1)} points${a.cls === "small" ? ", too uncertain to shade" : ""}.`;
  }
  function showDetail(d) {
    const el = $("detail");
    if (!d) { el.innerHTML = `<h2>District</h2><div class="empty">Hover over or tap a district to see its numbers and its history.</div>`; return; }
    const v = vals.get(d.id);
    let big = "";
    if (v.cls !== "nohist" && v.cls !== "small") big = S.mode === "year" ? pct(v.v) : S.mode === "acs" ? `${pct(v.v)} <small>\u00b1${v.moe.toFixed(1)}</small>` : pts(v.v);
    const since = d.first >= 0 ? YEARS[d.first] : null;
    const notes = [];
    if (since !== null) notes.push(since === YEARS[0] ? `Comparable history back to ${YEARS[0]}.` : `Comparable history since ${since}. Before that, the district's boundaries were different.`);
    if (d.m) notes.push(`Figures through ${d.m} add up the former districts that make up today's district.`);
    if (d.hs && byId.get(d.hs)) {
      const h = byId.get(d.hs), hv = vals.get(h.id);
      const hvTxt = hv.cls === "nohist" || hv.cls === "small" ? "" : ` (${S.mode === "change" ? pts(hv.v) : pct(hv.v)})`;
      notes.push(`High school grades are served by ${h.n}${hvTxt}, outlined in gray.`);
    }
    el.innerHTML = `<h2>District</h2><div class="name">${esc(d.n)}</div><div class="meta">${DATA.states[d.s][1]} &middot; ${LAYER_NAME[d.l]}</div>`
      + (big ? `<div class="big">${big}</div>` : "") + `<div class="counts">${esc(valueText(d, v))}</div>`
      + (S.mode !== "acs" ? `<div class="acsline">${esc(acsLine(d))}</div>` : "")
      + (S.mode === "acs" ? ""   // the ACS view is a single 2020-2024 period: no SAIPE history chart or history notes
        : `<div class="cap">Official poverty rate, ages 5 to 17 (SAIPE)</div>` + spark(d) + `<div class="hist">${notes.map(esc).join(" ")}</div>`);
  }

  // ---------- legend ----------
  function legend() {
    const el = $("legend");
    const title = S.mode === "year" ? `Child poverty rate, ages 5 to 17, ${YEARS[S.yi]}`
      : S.mode === "acs" ? `Ages 6 to 17 below twice the poverty line, ${ACS.period} (ACS)`
      : `Change in points, ${WINDOWS[S.from].label} to ${WINDOWS[S.to].label}`;
    const cols = S.mode === "year" ? C.rate : S.mode === "acs" ? C.acs : C.chg;
    const edges = S.mode === "year" ? RATE_BINS.map((b) => b + "%") : S.mode === "acs" ? ACS_BINS.map((b) => b + "%")
      : CHG_BINS.map((b) => (b > 0 ? "+" : b < 0 ? "\u2212" : "") + Math.abs(b));
    let h = `<h2>${esc(title)}</h2><div class="strip">${cols.map((c) => `<span style="background:${c}"></span>`).join("")}</div>`;
    h += `<div class="ticks">${edges.map((t, i) => `<span style="left:${((i + 1) / cols.length) * 100}%">${t}</span>`).join("")}</div>`;
    const smallTxt = S.mode === "acs" ? `Too uncertain: margin of error over \u00b1${ACS.moe_max} points` : `Fewer than ${MAP_FLOOR} children${S.mode === "change" ? " a year" : ""}`;
    const noTxt = S.mode === "acs" ? "No ACS figure (boundaries changed)" : "No comparable figure (boundaries changed)";
    h += `<div class="row"><span class="sw" style="background:${S.mode === "acs" ? C.unc : C.small}"></span>${smallTxt}</div>`;
    h += `<div class="row"><span class="sw" style="background:repeating-linear-gradient(135deg,${C.nohist} 0 3px,${C.hatch} 3px 4.5px)"></span>${noTxt}</div>`;
    el.innerHTML = h;
  }

  // ---------- headline ----------
  function headline() {
    const inState = (d) => !S.st || d.s === S.st;
    const where = S.st ? DATA.states[S.st][1] : "the United States";
    if (S.mode === "year") {
      let k = 0, p = 0, n = 0, all = 0;
      // all layers: SAIPE splits children by grade span where elementary and secondary districts overlap,
      // so the elementary + secondary counts together cover every child in that area
      for (const d of D) {
        if (!inState(d)) continue;
        all++;
        if (d.k[S.yi] !== null) { k += d.k[S.yi]; p += d.p[S.yi]; n++; }
      }
      const y = YEARS[S.yi];
      const cover = n === all ? `all ${nf.format(n)} districts` : `the ${nf.format(n)} of ${nf.format(all)} districts with a comparable figure`;
      $("sub").textContent = k ? `${S.st ? where : "United States"}, ${y}: ${pct((100 * p) / k)} of children ages 5 to 17 in ${cover} lived in families in poverty (${nf.format(p)} of ${nf.format(k)}).` : "";
    } else if (S.mode === "acs") {
      // unified, elementary and Vermont unions tile the map; secondary districts overlap elementary ones
      let k = 0, b = 0, n = 0, all = 0;
      for (const d of D) {
        if (!inState(d) || d.l === "s") continue;
        all++;
        if (d.a) { k += d.a[2]; b += d.a[3]; }
        const v = vals.get(d.id);
        if (v.cls !== "nohist" && v.cls !== "small") n++;
      }
      $("sub").textContent = k ? `${S.st ? where : "United States"}, ${ACS.period}: ${pct((100 * b) / k)} of children ages 6 to 17 lived below twice the poverty line (ACS estimate). ${nf.format(n)} of ${nf.format(all)} districts have a margin of error small enough to shade.` : "";
    } else {
      let n = 0, down = 0, up = 0, all = 0;
      for (const d of D) {
        if (!inState(d)) continue;
        all++;
        const v = vals.get(d.id);
        if (v.cls === "nohist") continue;
        if (v.cls === "small") continue;
        n++; if (v.v <= -2) down++; if (v.v >= 2) up++;
      }
      $("sub").textContent = `${S.st ? where : "United States"}, from ${WINDOWS[S.from].label} to ${WINDOWS[S.to].label}: of ${nf.format(n)} districts with comparable figures and at least ${MAP_FLOOR} children, the pooled rate fell by 2 points or more in ${nf.format(down)} and rose by 2 points or more in ${nf.format(up)}.`;
    }
  }

  // ---------- rankings ----------
  function rankings() {
    const el = $("rank");
    const tabs = S.mode === "change" ? ["Largest drops", "Largest increases"] : ["Highest", "Lowest"];
    const scope = S.st ? DATA.states[S.st][1] : "All states";
    const rows = [];
    for (const d of fillList.concat(secList)) {
      if (S.st && d.s !== S.st) continue;
      const v = vals.get(d.id);
      if (v.cls === "nohist" || v.cls === "small") continue;
      if (S.mode === "change" ? (v.a.avgK < RANK_FLOOR || v.b.avgK < RANK_FLOOR) : v.k < RANK_FLOOR) continue;
      rows.push([d, v]);
    }
    const sign = S.mode === "change" ? (S.rankTab === 0 ? 1 : -1) : (S.rankTab === 0 ? -1 : 1);
    rows.sort((a, b) => sign * (a[1].v - b[1].v) || a[0].n.localeCompare(b[0].n));
    let h = `<h2>Rankings</h2><div class="tabs">${tabs.map((t, i) => `<button type="button" data-t="${i}" aria-pressed="${i === S.rankTab}">${t}</button>`).join("")}</div>`;
    const what = S.mode === "year" ? `${YEARS[S.yi]}, districts with ${RANK_FLOOR} or more children`
      : S.mode === "acs" ? `ACS ${ACS.period}, districts with ${RANK_FLOOR} or more children ages 6 to 17 and a margin of error of \u00b1${ACS.moe_max} points or less. Read ranks as rough: most margins are several points wide`
      : `${WINDOWS[S.from].label} to ${WINDOWS[S.to].label}, districts with ${RANK_FLOOR} or more children a year in both periods`;
    h += `<p class="scope">${esc(scope)}: ${esc(what)}. ${nf.format(rows.length)} qualify.`
      + (S.mode === "change" ? " Each period's rate is pooled: three years of children in poverty divided by three years of children (our calculation from the Census figures). Blue on the map means fewer children in poverty." : "") + `</p>`;
    if (rows.length < 5) {
      h += `<p class="msg">Not enough qualifying districts to rank here.</p>`;
    } else {
      h += "<table>" + rows.slice(0, TOP_N).map(([d, v], i) => {
        const val = S.mode === "year" ? pct(v.v) : S.mode === "acs" ? `${pct(v.v)}<br><small>\u00b1${v.moe.toFixed(1)}</small>` : pts(v.v);
        const sub = S.mode === "year" ? `${nf.format(v.p)} of ${nf.format(v.k)}` : S.mode === "acs" ? `${nf.format(v.b)} of ${nf.format(v.k)}` : `${pct(v.a.rate)} to ${pct(v.b.rate)}`;
        return `<tr data-id="${d.id}"${S.sel === d ? ' class="sel"' : ""}><td class="r">${i + 1}</td><td>${esc(d.n)}${S.st ? "" : `, ${stAbbr(d.s)}`}<br><small>${sub}</small></td><td class="n">${val}</td></tr>`;
      }).join("") + "</table>";
    }
    el.innerHTML = h;
    el.querySelectorAll(".tabs button").forEach((b) => (b.onclick = () => { S.rankTab = +b.dataset.t; rankings(); }));
    el.querySelectorAll("tr[data-id]").forEach((tr) => (tr.onclick = () => select(byId.get(tr.dataset.id), true)));
  }

  // ---------- selection ----------
  function select(d, zoom) {
    S.sel = d;
    showDetail(d);
    if (d && zoom && d.bb) {
      const pad = Math.max(d.bb[2] - d.bb[0], d.bb[3] - d.bb[1]) * 1.5;
      fitBox([d.bb[0] - pad, d.bb[1] - pad, d.bb[2] + pad, d.bb[3] + pad], 0.05, homeK * 300);
    }
    rankings();
    if (d && zoom && d.bb) draw(); else drawOverlay();
  }

  // ---------- controls ----------
  function setMode(m) {
    S.mode = m; S.rankTab = 0;
    $("vYear").setAttribute("aria-pressed", m === "year");
    $("vChange").setAttribute("aria-pressed", m === "change");
    $("vAcs").setAttribute("aria-pressed", m === "acs");
    $("yearCtl").hidden = m !== "year";
    $("fromCtl").hidden = $("toCtl").hidden = m !== "change";
    update();
  }
  function update() {
    computeVals(); legend(); headline(); rankings(); showDetail(S.hover || S.sel);
    $("yearOut").textContent = YEARS[S.yi];
    draw();
  }
  $("vYear").onclick = () => { stopPlay(); setMode("year"); };
  $("vChange").onclick = () => { stopPlay(); setMode("change"); };
  $("vAcs").onclick = () => { stopPlay(); setMode("acs"); };
  const yr = $("year");
  yr.max = NY - 1; yr.value = S.yi;
  yr.oninput = () => { S.yi = +yr.value; update(); };
  let playT = null, speed = 1;
  const STEP_MS = 900;
  function stopPlay() { if (playT) { clearInterval(playT); playT = null; $("play").textContent = "Play"; } }
  function startTimer() {
    clearInterval(playT);
    playT = setInterval(() => { if (S.yi >= NY - 1) return stopPlay(); S.yi++; yr.value = S.yi; update(); }, STEP_MS / speed);
  }
  $("play").onclick = () => {
    if (playT) return stopPlay();
    if (S.yi === NY - 1) S.yi = 0;
    $("play").textContent = "Pause";
    yr.value = S.yi; update();
    startTimer();
  };
  $("speed").onclick = () => {
    speed = speed === 3 ? 1 : speed + 1;
    $("speed").textContent = speed + "x";
    $("speed").setAttribute("aria-label", `Play speed ${speed} times`);
    if (playT) startTimer();
  };
  const fromSel = $("from"), toSel = $("to");
  WINDOWS.forEach((w, i) => { fromSel.add(new Option(w.label, i)); toSel.add(new Option(w.label, i)); });
  fromSel.value = S.from; toSel.value = S.to;
  fromSel.onchange = () => { S.from = +fromSel.value; update(); };
  toSel.onchange = () => { S.to = +toSel.value; update(); };
  const stSel = $("state");
  Object.entries(DATA.states).sort((a, b) => a[1][1].localeCompare(b[1][1])).forEach(([f, [ab, nm]]) => stSel.add(new Option(nm, f)));
  stSel.onchange = () => { S.st = stSel.value; home(); update(); };
  $("reset").onclick = () => {
    stopPlay(); S.st = ""; stSel.value = ""; S.sel = null; S.hover = null; S.yi = NY - 1; yr.value = S.yi;
    S.from = defaultFrom; S.to = defaultTo; fromSel.value = S.from; toSel.value = S.to; hideTip(); home(); setMode("year");
  };

  // search
  const q = $("q"), lb = $("lb");
  const searchIdx = D.map((d) => [d, (d.n + " " + DATA.states[d.s][0] + " " + DATA.states[d.s][1]).toLowerCase()]);
  let hits = [], act = -1;
  function renderLb() {
    lb.innerHTML = hits.map((d, i) => `<li role="option" id="o${i}" data-i="${i}" aria-selected="${i === act}">${esc(d.n)} <small>${stAbbr(d.s)}</small></li>`).join("");
    lb.hidden = !hits.length; q.setAttribute("aria-expanded", String(!!hits.length));
    lb.querySelectorAll("li").forEach((li) => (li.onmousedown = (e) => { e.preventDefault(); choose(hits[+li.dataset.i]); }));
  }
  function choose(d) { q.value = d.n; hits = []; renderLb(); select(d, true); }
  q.oninput = () => {
    const t = q.value.trim().toLowerCase();
    act = -1;
    hits = t.length < 2 ? [] : searchIdx.filter(([d, s]) => s.includes(t) && (!S.st || d.s === S.st)).slice(0, 12).map((x) => x[0]);
    renderLb();
  };
  q.onkeydown = (e) => {
    if (e.key === "ArrowDown" && hits.length) { act = Math.min(hits.length - 1, act + 1); renderLb(); e.preventDefault(); }
    else if (e.key === "ArrowUp" && hits.length) { act = Math.max(0, act - 1); renderLb(); e.preventDefault(); }
    else if (e.key === "Enter" && hits.length) { choose(hits[Math.max(0, act)]); e.preventDefault(); }
    else if (e.key === "Escape") { hits = []; renderLb(); }
  };
  q.onblur = () => setTimeout(() => { hits = []; renderLb(); }, 100);

  // theme changes repaint
  const mq = window.matchMedia("(prefers-color-scheme: dark)");
  (mq.addEventListener ? mq.addEventListener("change", () => { readColors(); update(); }) : null);

  // ---------- start ----------
  readColors();
  computeVals();
  $("loading").remove();
  new ResizeObserver(resize).observe(wrap);
  const hs = new URLSearchParams(location.hash.slice(1));
  if (hs.get("view") === "change" || hs.get("view") === "acs") setMode(hs.get("view")); else update();
  if (hs.get("debug") === "1") window.__cpdbg = { hoverAt, render, renderBase, W: () => W, H: () => H };
  if (hs.get("d") && byId.get(hs.get("d"))) { pendingSel = byId.get(hs.get("d")); if (W) { select(pendingSel, true); pendingSel = null; } }
})().catch((e) => {
  const s = document.getElementById("sub");
  if (s) s.textContent = "The map could not load: " + e.message;
  throw e;
});
