"""Cartoon of the paper's Figures 2 and 5, version 2: real email snippets instead of counts.

Panel 1 (raw generator score) shows the two emails from paper Figure 2 as text, with their
[placeholders] highlighted: the correct one has many, the failing one only two.
Panels 2 and 3 show the same two emails as small thumbnails (many vs two placeholder chips).

Dot positions are schematic; rho values are the real ones for this prompt (paper Figure 5).
Email text is quoted from paper Figure 2 (shortened with ellipses).

Run:  python make_cartoon_figure_v2.py  -> figures/cartoon-idea-v2.html
Then: node render_figure.js figures/cartoon-idea-v2.html  -> .pdf (vector) and .png (transparent)
"""
from pathlib import Path

OUT = Path(__file__).parent / "figures" / "cartoon-idea-v2.html"
W, H = 1780, 725                         # px; same size as version 1

INK, MUTED, GREEN, RED, BLUE, ORANGE = "#14161A", "#4A4F57", "#2E8B57", "#C8483A", "#2F5D9B", "#D2601A"
CHIP_BG, CHIP_INK, LINE_GREY, GHOST = "#FBE3D2", "#A8440F", "#C9CDD3", "#9AA1AA"
FONT = "Archivo, 'Helvetica Neue', sans-serif"
MATH = "'STIX Two Text', 'Times New Roman', serif"

PLOT_Y, PLOT_H, PAD = 182, 410, 46
PANELS_X = [(0, 640), (760, 450), (1330, 450)]      # (left, width); panel 1 is wider for the text

# Email text from paper Figure 2. "[...]" segments are placeholders.
CORRECT_EMAIL = ["Dear [Customer Service Team/Name],",
                 "I recently purchased [product name], …",
                 "… While the [specific item] are …"]
WRONG_EMAIL = ["Hi [Recipient’s Name],",
               "I wanted to share my thoughts on the",
               "boots. They are warm, but I find them …",
               "Best regards, [Your Name]"]

# Schematic points, (x = generator score, y = validator), 0..1 within each plot.
PANELS = [
    dict(title="Raw generator score", rho="−0.24",
         correct=[(0.10, 0.55), (0.30, 0.50), (0.97, 0.60)], hl_c=(0.06, 0.92),
         wrong=[(0.04, 0.20), (0.04, 0.02)], hl_w=(0.94, 0.10),
         note=["The correct email is unlikely", "under the generator"]),
    dict(title="Frequency-corrected", rho="0.64",
         correct=[(0.50, 0.62), (0.90, 0.60), (0.60, 0.50)], hl_c=(0.72, 0.74),
         wrong=[(0.06, 0.34), (0.12, 0.04)], hl_w=(0.24, 0.12),
         ghost_c=(0.06, 0.92), ghost_w=(0.94, 0.10), trend=True,
         note=["Frequency correction pushes it up"]),
    dict(title="After FLORA training", rho="0.75",
         correct=[(0.66, 0.68), (0.92, 0.92), (0.78, 0.60)], hl_c=(0.80, 0.84),
         wrong=[(0.30, 0.26), (0.06, 0.24), (0.40, 0.06)], hl_w=(0.16, 0.10),
         trend=True,
         note=["Generator agrees with validator"]),
]
# Card boxes in figure px: (left, top, width, height). Panel 1: full text; panels 2-3: thumbnails.
CARDS = [
    dict(c=(193, 220, 386, 118), w=(140, 392, 394, 140), full=True),
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


def email_html(lines):
    out = []
    for line in lines:
        parts, buf, chip = [], "", False
        for ch in line:
            if ch == "[":
                parts.append(buf); buf = "["; chip = True
            elif ch == "]" and chip:
                buf += "]"; parts.append(f'<span class="chip">{buf}</span>'); buf = ""; chip = False
            else:
                buf += ch
        parts.append(buf)
        out.append(f'<div class="ln">{"".join(parts)}</div>')
    return "".join(out)


def thumb_html(chip_rows):
    """Email thumbnail: grey text lines with orange placeholder chips. chip_rows: list of rows,
    each a list of segment widths, positive = text, negative = chip."""
    rows = []
    for segs in chip_rows:
        cells = "".join(f'<span class="{"tchip" if s < 0 else "tline"}" style="width: {abs(s)}px"></span>' for s in segs)
        rows.append(f'<div class="trow">{cells}</div>')
    return "".join(rows)


MAIL_ICON = ('<svg class="mail" width="30" height="22" viewBox="0 0 30 22" aria-hidden="true">'
             '<rect x="1.5" y="1.5" width="27" height="19" rx="3" fill="#FFFFFF" stroke="' + INK + '" stroke-width="3"/>'
             '<path d="M 2 3 L 15 13 L 28 3" fill="none" stroke="' + INK + '" stroke-width="3" stroke-linejoin="round"/></svg>')
THUMB_CORRECT = [[30, -26, 34], [-22, 20, -28, 18], [24, -30, -20], [40, -24]]   # many chips
THUMB_WRONG = [[30, -34, 24], [92], [86], [40, -30]]                               # two chips

svg, html = [], []
svg.append(f'<rect x="2" y="2" width="{W-4}" height="74" rx="37" fill="#FFFFFF" stroke="{INK}" stroke-width="3"/>')
svg.append(t(40, 49, 'Prompt: “Rewrite this as an <tspan font-weight="700">email</tspan> with '
             '<tspan font-weight="700">at least 10 [placeholders]</tspan>: The boots are warm but a little uncomfortable.”', 27))

for k, (P, (x0, w), C) in enumerate(zip(PANELS, PANELS_X, CARDS)):
    ax0, ay0, ax1, ay1 = axes(x0, w)
    svg.append(t(x0 + w / 2, 128, f'{k+1}  {P["title"]}', 31, BLUE if k else INK, "middle", 700))
    svg.append(t(x0 + w / 2, 164, f'<tspan font-family="{MATH}" font-style="italic">ρ</tspan> = {P["rho"]}', 27, MUTED, "middle"))
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
    # Cards (HTML, drawn over the SVG), each with its badge at the top-right corner.
    for key, good in (("c", True), ("w", False)):
        l, tp, cw, ch = C[key]
        if C["full"]:
            count = "17 placeholders" if good else "2 placeholders"   # paper Figure 2
            inner = (MAIL_ICON + '<div class="body">' + email_html(CORRECT_EMAIL if good else WRONG_EMAIL)
                     + f'<div class="count">{count}</div></div>')
        else:
            inner = thumb_html(THUMB_CORRECT if good else THUMB_WRONG)
        cls = "card full" if C["full"] else "card thumb"
        html.append(f'<div class="{cls}" style="left: {l}px; top: {tp}px; width: {cw}px; height: {ch}px">{inner}</div>')
        badge = check_badge(l + cw - 2, tp + 2, 13) if good else cross_badge(l + cw - 2, tp + 2, 13)
        html.append(f'<svg class="badge" style="left: {l + cw - 18}px; top: {tp - 14}px" width="32" height="32" '
                    f'viewBox="{l + cw - 18} {tp - 14} 32 32">{badge}</svg>')
    for i, line in enumerate(P["note"]):
        svg.append(t(x0 + w / 2, PLOT_Y + PLOT_H + 44 + i * 32, line, 25, INK, "middle", 700))

for k, (label1, label2) in enumerate([("correct for", "frequency"), ("train with", "FLORA")]):
    gx = PANELS_X[k][0] + PANELS_X[k][1]
    gap = PANELS_X[k + 1][0] - gx
    my = PLOT_Y + PLOT_H / 2
    svg.append(arrow(gx + 14, my, gx + gap - 14, my, ORANGE, 7, "heado"))
    svg.append(t(gx + gap / 2, my - 52, label1, 22, ORANGE, "middle", 700))
    svg.append(t(gx + gap / 2, my - 26, label2, 22, ORANGE, "middle", 700))

svg.append(t(W - 4, H - 6, 'Emails from paper Fig. 2; dot positions schematic; ρ values from Fig. 5 (Gemma-2-9b-it).', 20, MUTED, "end"))

defs = f"""<defs>
<marker id="head" orient="auto" markerWidth="6" markerHeight="6" refX="3" refY="3"><path d="M0 0 L6 3 L0 6 Z" fill="{INK}"/></marker>
<marker id="headg" orient="auto" markerWidth="5" markerHeight="5" refX="2.5" refY="2.5"><path d="M0 0 L5 2.5 L0 5 Z" fill="{GHOST}"/></marker>
<marker id="heado" orient="auto" markerWidth="4" markerHeight="4" refX="1.5" refY="2"><path d="M0 0 L4 2 L0 4 Z" fill="{ORANGE}"/></marker>
</defs>"""

page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>The idea, as a cartoon (with emails)</title>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;700&amp;family=STIX+Two+Text:ital,wght@0,400;1,400&amp;display=swap" rel="stylesheet">
<style>
html, body {{ margin: 0; background: transparent }}
#figure {{ position: relative; width: {W}px; height: {H}px; font-family: {FONT}; color: {INK} }}
#figure > svg.main {{ position: absolute; left: 0; top: 0 }}
.card {{ position: absolute; box-sizing: border-box; background: #FFFFFF; border: 3px solid {INK}; border-radius: 14px }}
.card.full {{ padding: 10px 14px; font-size: 17px; line-height: 23px; white-space: nowrap; overflow: hidden; display: flex; gap: 10px; align-items: flex-start }}
.mail {{ flex: none; margin-top: 2px }}
.count {{ font-size: 14px; line-height: 18px; color: {MUTED}; margin-top: 3px }}
.chip {{ background: {CHIP_BG}; color: {CHIP_INK}; font-weight: 700; border-radius: 4px; padding: 0 1px }}
.card.thumb {{ padding: 10px 14px; display: flex; flex-direction: column; gap: 6px }}
.trow {{ display: flex; gap: 5px; height: 8px }}
.tline {{ display: block; height: 8px; border-radius: 4px; background: {LINE_GREY} }}
.tchip {{ display: block; height: 8px; border-radius: 4px; background: {ORANGE} }}
.badge {{ position: absolute; overflow: visible }}
</style>
</head>
<body>
<div id="figure">
<svg class="main" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Three-panel cartoon: the raw generator prefers a short email with two placeholders over a correct email with many; frequency correction reorders them; after FLORA training the generator agrees with the validator" style="overflow: visible">
{defs}
{chr(10).join(svg)}
</svg>
{chr(10).join(html)}
</div>
</body>
</html>
"""

if __name__ == "__main__":
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(page)
    print("wrote", OUT)
