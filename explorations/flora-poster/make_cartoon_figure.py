"""Cartoon version of the paper's Figures 2 and 5: one IFEval prompt, three stages.

Panel 1 (raw generator score): no relation to the validator; a short, generic email that
fails the prompt gets the highest generator score, a long correct email a low one.
Panel 2 (frequency-corrected score): the two swap order and a trend appears.
Panel 3 (after FLORA training): correct answers top right, wrong ones bottom left.

Dot positions are schematic (individual points in the paper's figure cannot be identified);
the rho values are the real ones for this prompt (paper Figure 5: -0.24, 0.64, 0.75).

Run:  python make_cartoon_figure.py  -> figures/cartoon-idea.html
Then: node render_figure.js figures/cartoon-idea.html  -> .pdf (vector) and .png (transparent)
"""
from pathlib import Path

OUT = Path(__file__).parent / "figures" / "cartoon-idea.html"
W, H = 1780, 725                         # px; 1335 x 544 pt, the Figure 5 slot in the banner

INK, MUTED, GREEN, RED, BLUE, ORANGE = "#14161A", "#4A4F57", "#2E8B57", "#C8483A", "#2F5D9B", "#D2601A"
CARD, GHOST = "#FFFFFF", "#9AA1AA"
FONT = "Archivo, 'Helvetica Neue', sans-serif"
MATH = "'STIX Two Text', 'Times New Roman', serif"

PANEL_W, PANEL_GAP = 506, 131
PLOT_Y, PLOT_H = 182, 410
PAD = 46                                  # inner padding of each plot for the axes

# Schematic points (x = generator score, y = validator, both 0..1). "hl" marks the two emails.
PANELS = [   # card_c / card_w: top-left corner of each email card, in the same 0..1 plot units
    dict(title="Raw generator score", rho="−0.24",
         correct=[(0.06, 0.58), (0.30, 0.66), (0.42, 0.56)], hl_c=(0.16, 0.80), card_c=(0.30, 1.00),
         wrong=[(0.24, 0.26), (0.44, 0.12), (0.08, 0.16)], hl_w=(0.90, 0.12), card_w=(0.52, 0.44),
         note="Generator prefers the failing email"),
    dict(title="Frequency-corrected", rho="0.64",
         correct=[(0.50, 0.62), (0.92, 0.62), (0.62, 0.52)], hl_c=(0.74, 0.70), card_c=(0.42, 1.00),
         wrong=[(0.36, 0.32), (0.44, 0.14), (0.10, 0.30)], hl_w=(0.24, 0.12), card_w=(0.52, 0.46),
         ghost_c=(0.16, 0.80), ghost_w=(0.90, 0.12), trend=True,
         note="Common text loses its head start"),
    dict(title="After FLORA training", rho="0.75",
         correct=[(0.66, 0.68), (0.90, 0.90), (0.78, 0.62)], hl_c=(0.82, 0.82), card_c=(0.06, 1.00),
         wrong=[(0.30, 0.26), (0.06, 0.24), (0.34, 0.08)], hl_w=(0.16, 0.10), card_w=(0.40, 0.46),
         trend=True,
         note="Generator agrees with validator"),
]


def t(x, y, s, size=26, fill=INK, anchor="start", weight=400, family=FONT, style=""):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" '
            f'font-weight="{weight}" font-family="{family}" {style}>{s}</text>')


def check_badge(cx, cy, r=15, fill=GREEN):
    return (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{fill}" stroke="{INK}" stroke-width="3"/>'
            f'<path d="M {cx - r*0.45:.1f} {cy:.1f} L {cx - r*0.1:.1f} {cy + r*0.38:.1f} L {cx + r*0.5:.1f} {cy - r*0.4:.1f}" '
            f'fill="none" stroke="#FFFFFF" stroke-width="{r*0.28:.1f}" stroke-linecap="round" stroke-linejoin="round"/>')


def cross_badge(cx, cy, r=15, fill=RED):
    d = r * 0.4
    return (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{fill}" stroke="{INK}" stroke-width="3"/>'
            f'<path d="M {cx-d:.1f} {cy-d:.1f} L {cx+d:.1f} {cy+d:.1f} M {cx+d:.1f} {cy-d:.1f} L {cx-d:.1f} {cy+d:.1f}" '
            f'stroke="#FFFFFF" stroke-width="{r*0.28:.1f}" stroke-linecap="round"/>')


def ghost(cx, cy, r=15):
    return f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="none" stroke="{GHOST}" stroke-width="3" stroke-dasharray="5 5"/>'


def arrow(x1, y1, x2, y2, color=MUTED, width=4, mid=""):
    return (f'<path d="M {x1:.1f} {y1:.1f} L {x2:.1f} {y2:.1f}" stroke="{color}" stroke-width="{width}" '
            f'fill="none" stroke-linecap="round" marker-end="url(#{mid or "head"})"/>')


CARD_H = 58


def card_width(label):
    return 72 + round(len(label) * 12.8)          # icon + text at 22px bold (Archivo) + padding


def envelope_card(x, y, label, good):
    """Cartoon email card: envelope icon, label, and a check/cross badge."""
    w, h = card_width(label), CARD_H
    icon = (f'<rect x="{x+12}" y="{y+16}" width="34" height="26" rx="4" fill="#FFFFFF" stroke="{INK}" stroke-width="3"/>'
            f'<path d="M {x+12} {y+18} L {x+29} {y+31} L {x+46} {y+18}" fill="none" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>')
    badge = check_badge(x + w - 2, y + 2, 13) if good else cross_badge(x + w - 2, y + 2, 13)
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{CARD}" stroke="{INK}" stroke-width="3"/>'
            + icon + t(x + 58, y + 37, label, 22, INK, weight=700) + badge)


parts = []
# Prompt bubble across the top.
parts.append(f'<rect x="2" y="2" width="{W-4}" height="74" rx="37" fill="{CARD}" stroke="{INK}" stroke-width="3"/>')
parts.append(t(40, 49, 'Prompt: “Rewrite this as an <tspan font-weight="700">email</tspan> with '
               '<tspan font-weight="700">at least 10 [placeholders]</tspan>: The boots are warm but a little uncomfortable.”', 27))

for k, P in enumerate(PANELS):
    x0 = k * (PANEL_W + PANEL_GAP)
    # Title and rho.
    parts.append(t(x0 + PANEL_W / 2, 128, f'{k+1}  {P["title"]}', 31, BLUE if k else INK, "middle", 700))
    parts.append(t(x0 + PANEL_W / 2, 164, f'<tspan font-family="{MATH}" font-style="italic">ρ</tspan> = {P["rho"]}',
                   27, MUTED, "middle"))
    # Plot card and axes.
    parts.append(f'<rect x="{x0}" y="{PLOT_Y}" width="{PANEL_W}" height="{PLOT_H}" rx="26" fill="{CARD}" stroke="{INK}" stroke-width="4"/>')
    ax0, ay0 = x0 + PAD, PLOT_Y + PLOT_H - PAD          # axis origin
    ax1, ay1 = x0 + PANEL_W - 24, PLOT_Y + 26
    parts.append(arrow(ax0, ay0, ax1, ay0, INK, 4))
    parts.append(arrow(ax0, ay0, ax0, ay1, INK, 4))
    parts.append(t(ax1 - 6, ay0 + 32, 'generator likes it', 22, MUTED, "end"))
    parts.append(f'<text transform="translate({ax0 - 16},{ay1 + 4}) rotate(-90)" font-size="22" fill="{MUTED}" '
                 f'text-anchor="end" font-family="{FONT}">validator says correct</text>')

    def pos(p):
        px = ax0 + 22 + p[0] * (ax1 - ax0 - 50)
        py = ay0 - 22 - p[1] * (ay0 - ay1 - 50)
        return px, py

    if P.get("trend"):
        a, b = pos((0.05, 0.05)), pos((0.97, 0.97))
        parts.append(f'<path d="M {a[0]:.1f} {a[1]:.1f} L {b[0]:.1f} {b[1]:.1f}" stroke="{ORANGE}" stroke-width="5" '
                     f'stroke-dasharray="12 10" opacity="0.55" stroke-linecap="round"/>')
    if "ghost_c" in P:
        for g, h in ((P["ghost_c"], P["hl_c"]), (P["ghost_w"], P["hl_w"])):
            gx, gy = pos(g); hx, hy = pos(h)
            parts.append(ghost(gx, gy))
            dx, dy = hx - gx, hy - gy
            L = (dx * dx + dy * dy) ** 0.5
            parts.append(arrow(gx + dx / L * 20, gy + dy / L * 20, hx - dx / L * 22, hy - dy / L * 22, GHOST, 4, "headg"))
    for p in P["wrong"]:
        parts.append(cross_badge(*pos(p), 12))
    for p in P["correct"]:
        parts.append(check_badge(*pos(p), 12))
    # The two highlighted emails, bigger, with cards.
    cx, cy = pos(P["hl_c"]); wx, wy = pos(P["hl_w"])
    parts.append(check_badge(cx, cy, 17))
    parts.append(cross_badge(wx, wy, 17))
    def card_at(anchor, dot, label, good):
        kx, ky = pos(anchor)
        w = card_width(label)
        kx = min(kx, ax1 - w - 8)                   # keep the card inside the plot
        px, py = dot
        ty = ky + CARD_H if ky + CARD_H < py else ky   # attach the leader to the nearer card edge
        tx = min(max(px, kx + 20), kx + w - 20)
        line = f'<path d="M {px:.1f} {py:.1f} L {tx:.1f} {ty:.1f}" stroke="{INK}" stroke-width="3"/>'
        return line + envelope_card(kx, ky, label, good)
    parts.append(card_at(P["card_c"], (cx, cy), '17 placeholders', True))
    parts.append(card_at(P["card_w"], (wx, wy), '2 placeholders', False))
    # Panel takeaway.
    parts.append(t(x0 + PANEL_W / 2, PLOT_Y + PLOT_H + 44, P["note"], 25, INK, "middle", 700))

# Arrows between panels with labels.
for k, label in enumerate(["correct for", "train with"]):
    gx = (k + 1) * PANEL_W + k * PANEL_GAP
    my = PLOT_Y + PLOT_H / 2
    parts.append(arrow(gx + 14, my, gx + PANEL_GAP - 14, my, ORANGE, 7, "heado"))
    parts.append(t(gx + PANEL_GAP / 2, my - 52, label, 22, ORANGE, "middle", 700))
    parts.append(t(gx + PANEL_GAP / 2, my - 26, ["frequency", "FLORA"][k], 22, ORANGE, "middle", 700))

parts.append(t(W - 4, H - 6, 'Schematic of paper Figs. 2 and 5; ρ values from that prompt (Gemma-2-9b-it).', 20, MUTED, "end"))

defs = f"""<defs>
<marker id="head" orient="auto" markerWidth="6" markerHeight="6" refX="3" refY="3"><path d="M0 0 L6 3 L0 6 Z" fill="{INK}"/></marker>
<marker id="headg" orient="auto" markerWidth="5" markerHeight="5" refX="2.5" refY="2.5"><path d="M0 0 L5 2.5 L0 5 Z" fill="{GHOST}"/></marker>
<marker id="heado" orient="auto" markerWidth="4" markerHeight="4" refX="1.5" refY="2"><path d="M0 0 L4 2 L0 4 Z" fill="{ORANGE}"/></marker>
</defs>"""

html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>The idea, as a cartoon</title>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;700&amp;family=STIX+Two+Text:ital,wght@0,400;1,400&amp;display=swap" rel="stylesheet">
<style>html, body {{ margin: 0; background: transparent }}</style>
</head>
<body>
<div id="figure" style="width: {W}px; height: {H}px">
<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Three-panel cartoon: raw generator scores disagree with the validator; frequency correction reorders a short wrong email and a long correct email; after FLORA training the generator agrees with the validator" style="display: block; overflow: visible">
{defs}
{chr(10).join(parts)}
</svg>
</div>
</body>
</html>
"""

if __name__ == "__main__":
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(html)
    print("wrote", OUT)
