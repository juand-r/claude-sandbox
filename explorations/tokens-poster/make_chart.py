"""Results dot plot: BLiMP under the submitted recipe, only the tokenizer varies (paper Table 6).

Run:  python make_chart.py  -> figures/results.html
Then: node render_figure.js figures/results.html  -> .pdf (vector) and .png (transparent)
"""
from pathlib import Path

OUT = Path(__file__).parent / "figures" / "results.html"
W, H = 1000, 600
INK, MUTED, GRID, ORANGE, GREY = "#14161A", "#4A4F57", "#C9CDD3", "#D2601A", "#7A828C"
FONT = "Archivo, 'Helvetica Neue', sans-serif"

# Table 6: Muon + MNTP@20%, same recipe as the submitted model. (label, BLiMP, style)
ROWS = [
    ("Ours, submitted (pruned)", 72.53, "ours"),
    ("Unigram", 67.97, "other"),
    ("Ours, un-pruned", 67.71, "ours-light"),
    ("BPE", 67.11, "other"),
    ("Morfessor 2.0", 66.63, "other"),
    ("MorphPiece (raw MorphyNet)", 65.89, "other"),
]
X_MIN, X_MAX, X_TICKS = 64, 74, (64, 66, 68, 70, 72, 74)
LABEL_W, TOP, ROW_H, RIGHT_PAD = 470, 20, 80, 80


def x_of(v):
    return LABEL_W + (v - X_MIN) / (X_MAX - X_MIN) * (W - LABEL_W - RIGHT_PAD)


svg = []
axis_y = TOP + len(ROWS) * ROW_H + 10
for t in X_TICKS:
    x = x_of(t)
    svg.append(f'<line x1="{x:.1f}" y1="{axis_y - 10}" x2="{x:.1f}" y2="{axis_y}" stroke="{MUTED}" stroke-width="2"/>')
    svg.append(f'<text x="{x:.1f}" y="{axis_y + 34}" font-size="24" fill="{MUTED}" text-anchor="middle">{t}</text>')
svg.append(f'<line x1="{x_of(X_MIN):.1f}" y1="{axis_y}" x2="{x_of(X_MAX):.1f}" y2="{axis_y}" stroke="{MUTED}" stroke-width="2"/>')
svg.append(f'<text x="{x_of((X_MIN + X_MAX) / 2):.1f}" y="{axis_y + 72}" font-size="26" fill="{MUTED}" text-anchor="middle">BLiMP accuracy</text>')
for i, (label, v, style) in enumerate(ROWS):
    y = TOP + i * ROW_H + ROW_H / 2
    bold = 700 if style == "ours" else 400
    svg.append(f'<text x="{LABEL_W - 24}" y="{y + 9:.1f}" font-size="31" font-weight="{bold}" fill="{INK}" text-anchor="end">{label}</text>')
    svg.append(f'<line x1="{x_of(X_MIN):.1f}" y1="{y:.1f}" x2="{x_of(v):.1f}" y2="{y:.1f}" stroke="{GRID}" stroke-width="3" stroke-dasharray="2 8" stroke-linecap="round"/>')
    if style == "ours":
        dot = f'<circle cx="{x_of(v):.1f}" cy="{y:.1f}" r="15" fill="{ORANGE}"/>'
    elif style == "ours-light":
        dot = f'<circle cx="{x_of(v):.1f}" cy="{y:.1f}" r="13" fill="#FFFFFF" stroke="{ORANGE}" stroke-width="5"/>'
    else:
        dot = f'<circle cx="{x_of(v):.1f}" cy="{y:.1f}" r="13" fill="{GREY}"/>'
    svg.append(dot)
    svg.append(f'<text x="{x_of(v) + 26:.1f}" y="{y + 10:.1f}" font-size="30" font-weight="{bold}" fill="{ORANGE if style == "ours" else INK}">{v:.2f}</text>')

page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Tokenizer comparison (BLiMP)</title>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;700&amp;display=swap" rel="stylesheet">
<style>
html, body {{ margin: 0; background: transparent }}
#figure {{ position: relative; width: {W}px; height: {H}px; font-family: {FONT} }}
</style>
</head>
<body>
<div id="figure">
<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}" role="img" aria-label="BLiMP accuracy by tokenizer under the submitted training recipe: Ours submitted 72.53, Unigram 67.97, Ours un-pruned 67.71, BPE 67.11, Morfessor 66.63, MorphPiece 65.89">
{chr(10).join(svg)}
</svg>
</div>
</body>
</html>
"""

if __name__ == "__main__":
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(page)
    print("wrote", OUT)
