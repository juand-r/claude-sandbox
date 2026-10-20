"""Cartoon of the paper's Figures 2 and 5, version 4: the IFEval (a + b) / c prompt.

Same layout as version 3. The example is rankalign `data/fixed-prompts-ifeval/` prompt_11
("... in exactly two paragraphs, separated with the markdown divider: ***"). Panel 1 shows two
real answers from that file, shortened, with LaTeX shown as plain text: response_idx 36
(correct, two parts split by ***) and response_idx 70 (incorrect: right math, one paragraph).
Panels 2 and 3 show them as thumbnails (two blocks with a *** divider vs one block).

Dot positions are schematic. No rho values: the paper reports them only for the email prompt.

Run:  python make_cartoon_figure_v4.py  -> figures/cartoon-idea-v4.html
Then: node render_figure.js figures/cartoon-idea-v4.html  -> .pdf (vector) and .png (transparent)
"""
from pathlib import Path

OUT = Path(__file__).parent / "figures" / "cartoon-idea-v4.html"
W, H = 1780, 725                         # px; drawing area, same as version 1
MARGIN = 6                               # px around the drawing so the outer box strokes are not clipped

INK, MUTED, GREEN, RED, BLUE, ORANGE = "#14161A", "#4A4F57", "#2E8B57", "#C8483A", "#2F5D9B", "#D2601A"
LINE_GREY, GHOST = "#C9CDD3", "#9AA1AA"
FONT = "Archivo, 'Helvetica Neue', sans-serif"

PLOT_Y, PLOT_H, PAD = 182, 410, 46
PROMPT_SIZE = 24                         # the full prompt needs a smaller size than v3 to fit
PANELS_X = [(0, 640), (760, 450), (1330, 450)]      # (left, width); panel 1 is wider for the text

# Answers from rankalign prompt_11 (response_idx 36 and 70), shortened with ellipses.
DIVIDER = "***"
CORRECT_ANSWER = ["To solve the math problem, we start with three",
                  "numbers: a, b, and c. We know that a equals …",
                  DIVIDER,
                  "In short, we first added 10 and 30 to get 40, …"]
WRONG_ANSWER = ["To find the value of (a + b) / c where a = 10,",
                "b = 30, and c = 20, we first add a and b:",
                "10 + 30 = 40. Next, we divide this sum by c:",
                "40 / 20 = 2. …"]

# Schematic points, (x = generator score, y = validator), 0..1 within each plot.
PANELS = [
    dict(title="Raw generator score",
         correct=[(0.10, 0.55), (0.02, 0.70), (0.99, 0.46)], hl_c=(0.06, 0.92),
         wrong=[(0.04, 0.20), (0.04, 0.02)], hl_w=(0.98, 0.10),
         note=["The correct answer is unlikely", "under the generator"]),
    dict(title="Frequency-corrected",
         correct=[(0.46, 0.66), (0.90, 0.60), (0.58, 0.58)], hl_c=(0.72, 0.66),
         wrong=[(0.06, 0.34), (0.12, 0.04)], hl_w=(0.24, 0.12),
         ghost_c=(0.06, 0.92), ghost_w=(0.98, 0.10), trend=True,
         note=["Frequency correction pushes it up"]),
    dict(title="After FLORA training",
         correct=[(0.66, 0.68), (0.92, 0.92), (0.78, 0.60)], hl_c=(0.80, 0.84),
         wrong=[(0.30, 0.26), (0.06, 0.24)], hl_w=(0.16, 0.10),
         trend=True,
         note=["Generator agrees with validator"]),
]
# Card boxes in figure px: (left, top, width, height). Panel 1: full text; panels 2-3: thumbnails.
CARDS = [
    dict(c=(180, 212, 434, 142), w=(132, 394, 414, 140), full=True),
    dict(c=(1030, 222, 150, 72), w=(950, 398, 150, 72), full=False),
    dict(c=(1420, 222, 150, 72), w=(1560, 418, 150, 72), full=False),
]


def axes(x0, w):
    ax0, ay0 = x0 + PAD, PLOT_Y + PLOT_H - PAD
    ax1, ay1 = x0 + w - 24, PLOT_Y + 26
    return ax0, ay0, ax1, ay1


def pos(p, x0, w):
    ax0, ay0, ax1, ay1 = axes(x0, w)
    return ax0 + 22 + p[0] * (ax1 - ax0 - 50), ay0 - 22 - p[1] * (ay0 - ay1 - 50)


def t(x, y, s, size=26, fill=INK, anchor="start", weight=400, family=FONT):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" '
            f'font-weight="{weight}" font-family="{family}">{s}</text>')


def check_badge(cx, cy, r=15):
    return (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{GREEN}" stroke="{INK}" stroke-width="3"/>'
            f'<path d="M {cx - r*0.45:.1f} {cy:.1f} L {cx - r*0.1:.1f} {cy + r*0.38:.1f} L {cx + r*0.5:.1f} {cy - r*0.4:.1f}" '
            f'fill="none" stroke="#FFFFFF" stroke-width="{r*0.28:.1f}" stroke-linecap="round" stroke-linejoin="round"/>')


def cross_badge(cx, cy, r=15):
    d = r * 0.4
    return (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{RED}" stroke="{INK}" stroke-width="3"/>'
            f'<path d="M {cx-d:.1f} {cy-d:.1f} L {cx+d:.1f} {cy+d:.1f} M {cx+d:.1f} {cy-d:.1f} L {cx-d:.1f} {cy+d:.1f}" '
            f'stroke="#FFFFFF" stroke-width="{r*0.28:.1f}" stroke-linecap="round"/>')


def arrow(x1, y1, x2, y2, color=MUTED, width=4, head="head"):
    return (f'<path d="M {x1:.1f} {y1:.1f} L {x2:.1f} {y2:.1f}" stroke="{color}" stroke-width="{width}" '
            f'fill="none" stroke-linecap="round" marker-end="url(#{head})"/>')


def leader(dot, box):
    """Line from a dot to the nearest point on a card's border."""
    (px, py), (l, tp, w, h) = dot, box
    nx, ny = min(max(px, l), l + w), min(max(py, tp), tp + h)
    return f'<path d="M {px:.1f} {py:.1f} L {nx:.1f} {ny:.1f}" stroke="{INK}" stroke-width="3"/>'


def answer_html(good):
    return "".join(f'<div class="ln divider">{s}</div>' if s == DIVIDER else f'<div class="ln">{s}</div>'
                   for s in (CORRECT_ANSWER if good else WRONG_ANSWER))


def thumb_html(rows):
    """Answer thumbnail: grey text lines; a row of None is the *** divider (three orange dots)."""
    out = []
    for w in rows:
        if w is None:
            out.append('<div class="trow tdiv">' + '<span class="tdot"></span>' * 3 + '</div>')
        else:
            out.append(f'<div class="trow"><span class="tline" style="width: {w}px"></span></div>')
    return "".join(out)


DOC_ICON = ('<svg class="doc" width="22" height="28" viewBox="0 0 22 28" aria-hidden="true">'
            '<path d="M 1.5 1.5 H 14 L 20.5 8 V 26.5 H 1.5 Z" fill="#FFFFFF" stroke="' + INK + '" stroke-width="3" stroke-linejoin="round"/>'
            '<path d="M 6 13 H 16 M 6 18 H 16 M 6 23 H 12" stroke="' + INK + '" stroke-width="2.5" stroke-linecap="round"/></svg>')
THUMB_CORRECT = [118, 80, None, 96]   # paragraph, *** divider, paragraph
THUMB_WRONG = [118, 112, 120, 64]     # one paragraph

svg, html = [], []
svg.append(f'<rect x="2" y="2" width="{W-4}" height="74" rx="37" fill="#FFFFFF" stroke="{INK}" stroke-width="3"/>')
svg.append(t(40, 49, 'Prompt: “If a = 10, b = 30, and c = 20, what is the value of (a + b) / c? Give me the answer in '
             '<tspan font-weight="700">exactly two paragraphs</tspan>, separated with the markdown divider: '
             '<tspan font-weight="700">***</tspan>”', PROMPT_SIZE))

for k, (P, (x0, w), C) in enumerate(zip(PANELS, PANELS_X, CARDS)):
    ax0, ay0, ax1, ay1 = axes(x0, w)
    svg.append(t(x0 + w / 2, 150, f'{k+1}  {P["title"]}', 31, BLUE if k else INK, "middle", 700))
    svg.append(f'<rect x="{x0}" y="{PLOT_Y}" width="{w}" height="{PLOT_H}" rx="26" fill="#FFFFFF" stroke="{INK}" stroke-width="4"/>')
    svg.append(arrow(ax0, ay0, ax1, ay0, INK, 4))
    svg.append(arrow(ax0, ay0, ax0, ay1, INK, 4))
    svg.append(t(ax1 - 6, ay0 + 32, 'generator likes it', 22, MUTED, "end"))
    svg.append(f'<text transform="translate({ax0 - 16},{ay1 + 4}) rotate(-90)" font-size="22" fill="{MUTED}" '
               f'text-anchor="end" font-family="{FONT}">validator says correct</text>')
    P_ = lambda p: pos(p, x0, w)
    if P.get("trend"):
        a, b = P_((0.05, 0.05)), P_((0.97, 0.97))
        svg.append(f'<path d="M {a[0]:.1f} {a[1]:.1f} L {b[0]:.1f} {b[1]:.1f}" stroke="{ORANGE}" stroke-width="5" '
                   f'stroke-dasharray="12 10" opacity="0.55" stroke-linecap="round"/>')
    if "ghost_c" in P:
        for g, h in ((P["ghost_c"], P["hl_c"]), (P["ghost_w"], P["hl_w"])):
            (gx, gy), (hx, hy) = P_(g), P_(h)
            svg.append(f'<circle cx="{gx:.1f}" cy="{gy:.1f}" r="15" fill="none" stroke="{GHOST}" stroke-width="3" stroke-dasharray="5 5"/>')
            dx, dy = hx - gx, hy - gy
            L = (dx * dx + dy * dy) ** 0.5
            svg.append(arrow(gx + dx / L * 20, gy + dy / L * 20, hx - dx / L * 22, hy - dy / L * 22, GHOST, 4, "headg"))
    for p in P["wrong"]:
        svg.append(cross_badge(*P_(p), 12))
    for p in P["correct"]:
        svg.append(check_badge(*P_(p), 12))
    hc, hw = P_(P["hl_c"]), P_(P["hl_w"])
    svg.append(leader(hc, C["c"]))
    svg.append(leader(hw, C["w"]))
    svg.append(check_badge(*hc, 17))
    svg.append(cross_badge(*hw, 17))
    # Cards (HTML, drawn over the SVG). No corner badges: they read as extra data dots;
    # the connected dot already shows whether the answer is correct.
    for key, good in (("c", True), ("w", False)):
        l, tp, cw, ch = C[key]
        if C["full"]:
            count = "two paragraphs, split by ***" if good else "one paragraph, no ***"
            inner = (DOC_ICON + '<div class="body">' + answer_html(good)
                     + f'<div class="count">{count}</div></div>')
        else:
            inner = thumb_html(THUMB_CORRECT if good else THUMB_WRONG)
        cls = "card full" if C["full"] else "card thumb"
        html.append(f'<div class="{cls}" style="left: {l}px; top: {tp}px; width: {cw}px; height: {ch}px">{inner}</div>')
    for i, line in enumerate(P["note"]):
        svg.append(t(x0 + w / 2, PLOT_Y + PLOT_H + 44 + i * 32, line, 25, INK, "middle", 700))

for k, (label1, label2) in enumerate([("correct for", "frequency"), ("train with", "FLORA")]):
    gx = PANELS_X[k][0] + PANELS_X[k][1]
    gap = PANELS_X[k + 1][0] - gx
    my = PLOT_Y + PLOT_H / 2
    svg.append(arrow(gx + 14, my, gx + gap - 14, my, ORANGE, 7, "heado"))
    svg.append(t(gx + gap / 2, my - 52, label1, 22, ORANGE, "middle", 700))
    svg.append(t(gx + gap / 2, my - 26, label2, 22, ORANGE, "middle", 700))

svg.append(t(W - 4, H - 6, 'Answers from our IFEval data, shortened, math shown as plain text; dot positions schematic.', 20, MUTED, "end"))

defs = f"""<defs>
<marker id="head" orient="auto" markerWidth="6" markerHeight="6" refX="3" refY="3"><path d="M0 0 L6 3 L0 6 Z" fill="{INK}"/></marker>
<marker id="headg" orient="auto" markerWidth="5" markerHeight="5" refX="2.5" refY="2.5"><path d="M0 0 L5 2.5 L0 5 Z" fill="{GHOST}"/></marker>
<marker id="heado" orient="auto" markerWidth="4" markerHeight="4" refX="1.5" refY="2"><path d="M0 0 L4 2 L0 4 Z" fill="{ORANGE}"/></marker>
</defs>"""

page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>The idea, as a cartoon ((a + b) / c prompt)</title>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;700&amp;display=swap" rel="stylesheet">
<style>
html, body {{ margin: 0; background: transparent }}
#figure {{ position: relative; width: {W + 2 * MARGIN}px; height: {H + 2 * MARGIN}px; font-family: {FONT}; color: {INK} }}
.canvas {{ position: absolute; left: {MARGIN}px; top: {MARGIN}px; width: {W}px; height: {H}px }}
.canvas > svg.main {{ position: absolute; left: 0; top: 0 }}
.card {{ position: absolute; box-sizing: border-box; background: #FFFFFF; border: 3px solid {INK}; border-radius: 14px }}
.card.full {{ padding: 10px 14px; font-size: 17px; line-height: 23px; white-space: nowrap; overflow: hidden; display: flex; gap: 10px; align-items: flex-start }}
.doc {{ flex: none; margin-top: 0 }}
.divider {{ color: {ORANGE}; font-weight: 700; text-align: center; letter-spacing: 4px; font-size: 24px; line-height: 23px; padding-top: 3px }}
.count {{ font-size: 14px; line-height: 18px; color: {MUTED}; margin-top: 3px }}
.card.thumb {{ padding: 10px 14px; display: flex; flex-direction: column; gap: 6px }}
.trow {{ display: flex; gap: 5px; height: 8px }}
.tline {{ display: block; height: 8px; border-radius: 4px; background: {LINE_GREY} }}
.tdot {{ display: block; width: 8px; height: 8px; border-radius: 4px; background: {ORANGE} }}
.tdiv {{ justify-content: center }}
</style>
</head>
<body>
<div id="figure"><div class="canvas">
<svg class="main" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Three-panel cartoon: the raw generator prefers a one-paragraph answer over the requested two paragraphs split by ***; frequency correction reorders them; after FLORA training the generator agrees with the validator" style="overflow: visible">
{defs}
{chr(10).join(svg)}
</svg>
{chr(10).join(html)}
</div></div>
</body>
</html>
"""

MIN_GAP = 18   # px a dot must keep from any card it is not connected to, so each card's owner is clear


def check_clearance():
    def gap(pt, r, box):
        (x, y), (l, tp, w, h) = pt, box
        dx, dy = max(l - x, 0, x - (l + w)), max(tp - y, 0, y - (tp + h))
        return (dx * dx + dy * dy) ** 0.5 - r
    for k, (P, (x0, w), C) in enumerate(zip(PANELS, PANELS_X, CARDS)):
        dots = [(p, 12, None) for p in P["correct"] + P["wrong"]] + [(P["hl_c"], 17, "c"), (P["hl_w"], 17, "w")]
        for p, r, own in dots:
            for key in ("c", "w"):
                if key != own and gap(pos(p, x0, w), r, C[key]) < MIN_GAP:
                    raise ValueError(f"panel {k+1}: dot {p} is within {MIN_GAP}px of card {key}")


if __name__ == "__main__":
    check_clearance()
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(page)
    print("wrote", OUT)
