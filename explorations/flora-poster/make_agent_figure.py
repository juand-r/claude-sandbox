"""Poster version of the paper's Figure 3: the rational-agent model of generation.

The agent is unsure which answers are correct. It holds beliefs v (1 = believed correct),
each belief spreads probability over the answers it marks correct (pi(y | v, x)), and the
generator mixes them: p_G(y | x) = sum_v p(v | x) pi(y | v, x).

Bar heights are illustrative, as in the paper, but consistent: the generator row is the
weighted average of the two belief rows, drawn on the same scale.

Run:  python make_agent_figure.py  -> figures/agent-model.html
Then: node render_figure.js figures/agent-model.html  -> .pdf (vector) and .png (transparent)
"""
from pathlib import Path

OUT = Path(__file__).parent / "figures" / "agent-model.html"

W, H = 953, 420                     # px; 715 x 315 pt, the free space bottom-left on the A0 poster
ANSWERS = ["Helium", "Neon", "Radon", "Hydrogen", "Rn"]
BELIEFS = [                          # (validity vector v, pi(y | v, x)) as in the paper's Figure 3
    ([1, 1, 1, 0, 0], [0.60, 0.15, 0.25, 0.0, 0.0]),
    ([1, 1, 0, 0, 0], [0.50, 0.50, 0.0, 0.0, 0.0]),
]
WEIGHTS = [0.5, 0.5]                 # p(v | x); illustrative
MIX = [sum(w * pi[i] for w, (_, pi) in zip(WEIGHTS, BELIEFS)) for i in range(len(ANSWERS))]

INK, MUTED, BLUE, GREEN = "#14161A", "#4A4F57", "#2F5D9B", "#2E7D4F"
ZERO_FILL, ZERO_INK, RULE = "#E3E6EA", "#5F6670", "#C9CDD3"

LABEL_W, COL0, COL_W = 236, 252, 128     # label column, first answer column, column width
CELL_W, CELL_H = 92, 42
BAR_W, BAR_MAX = 64, 50
SCALE = BAR_MAX / max(max(pi) for _, pi in BELIEFS)   # one scale for every row

# Row tops (px). Each belief: cells, then its distribution; then the mixture.
Y_HEAD, Y_V1, Y_PI1, Y_V2, Y_PI2, Y_MIX_TEXT, Y_MIX_RULE, Y_PG = 0, 44, 94, 164, 214, 274, 312, 320

M = "font-family: 'STIX Two Text', 'Times New Roman', serif"
v = f'<b style="{M}; font-style: italic">v</b>'


def col_x(i):
    return COL0 + i * COL_W


def label(top, height, html, color=INK, weight=400):
    return (f'<div style="position: absolute; left: 0; top: {top}px; width: {LABEL_W}px; height: {height}px; '
            f'display: flex; align-items: center; justify-content: flex-end; text-align: right; '
            f'font-size: 25px; line-height: 1.15; color: {color}; font-weight: {weight}"><span>{html}</span></div>')


def cells(top, vec):
    out = []
    for i, bit in enumerate(vec):
        fill, ink = (GREEN, "#FFFFFF") if bit else (ZERO_FILL, ZERO_INK)
        x = col_x(i) + (COL_W - CELL_W) / 2
        out.append(f'<div style="position: absolute; left: {x:.0f}px; top: {top}px; width: {CELL_W}px; height: {CELL_H}px; '
                   f'border-radius: 8px; background: {fill}; color: {ink}; display: flex; align-items: center; '
                   f'justify-content: center; font-size: 26px; font-weight: 700">{bit}</div>')
    return out


def bars(top, probs, color=BLUE):
    base = top + BAR_MAX
    out = [f'<div style="position: absolute; left: {COL0 + 8}px; top: {base}px; width: {len(ANSWERS) * COL_W - 16}px; '
           f'height: 3px; background: {INK}"></div>']
    for i, p in enumerate(probs):
        if p <= 0:
            continue
        h = round(p * SCALE)
        x = col_x(i) + (COL_W - BAR_W) / 2
        out.append(f'<div style="position: absolute; left: {x:.0f}px; top: {base - h}px; width: {BAR_W}px; height: {h}px; '
                   f'background: {color}; border-radius: 6px 6px 0 0"></div>')
    return out


def pi_label(k):
    return f'<span style="{M}"><i>π</i>(<i>y</i> | {v}<sub style="font-size: .65em">{k}</sub>, <i>x</i>)</span>'


parts = []
# Header: what 1 means, and the answer names once.
parts.append(label(Y_HEAD, 34, '1 = believed correct', MUTED))
for i, name in enumerate(ANSWERS):
    parts.append(f'<div style="position: absolute; left: {col_x(i)}px; top: {Y_HEAD}px; width: {COL_W}px; height: 34px; '
                 f'text-align: center; font-size: 25px; line-height: 34px">{name}</div>')
for k, ((vec, pi), y_v, y_pi) in enumerate(zip(BELIEFS, (Y_V1, Y_V2), (Y_PI1, Y_PI2)), start=1):
    parts.append(label(y_v, CELL_H, f'Belief {v}<sub style="font-size: .65em">{k}</sub>', INK, 700))
    parts += cells(y_v, vec)
    parts.append(label(y_pi, BAR_MAX, pi_label(k)))
    parts += bars(y_pi, pi)
# Mixture: a rule across the columns, then the generator's distribution.
parts.append(f'<div style="position: absolute; left: {COL0 + 8}px; top: {Y_MIX_RULE}px; width: {len(ANSWERS) * COL_W - 16}px; '
             f'height: 0; border-top: 3px dashed {RULE}"></div>')
parts.append(f'<div style="position: absolute; left: {COL0 + 8}px; top: {Y_MIX_TEXT}px; font-size: 24px; line-height: 30px; color: {MUTED}">'
             f'mix the beliefs, weighted by <span style="{M}"><i>p</i>({v} | <i>x</i>)</span></div>')
parts.append(label(Y_PG, BAR_MAX + 4,
                   f'<span>Generator<br><span style="{M}"><i>p</i><sub style="font-size: .65em">G</sub>(<i>y</i> | <i>x</i>)</span></span>',
                   BLUE, 700))
parts += bars(Y_PG, MIX)
# Formula under the generator row.
parts.append(f'<div style="position: absolute; left: {COL0 + 8}px; top: {Y_PG + BAR_MAX + 12}px; font-size: 25px; {M}">'
             f'<i>p</i><sub style="font-size: .65em">G</sub>(<i>y</i> | <i>x</i>) = '
             f'Σ<sub style="font-size: .65em">{v}</sub> <i>p</i>({v} | <i>x</i>) <i>π</i>(<i>y</i> | {v}, <i>x</i>)</div>')

html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Agent model of generation</title>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;700&amp;family=STIX+Two+Text:ital,wght@0,400;0,700;1,400;1,700&amp;display=swap" rel="stylesheet">
<style>
@page {{ size: {W}px {H}px; margin: 0 }}
html, body {{ margin: 0; background: transparent }}
sub {{ vertical-align: -0.3em; line-height: 0 }}
</style>
</head>
<body>
<div id="figure" style="position: relative; width: {W}px; height: {H}px; overflow: hidden; color: {INK}; font-family: Archivo, 'Helvetica Neue', sans-serif">
{chr(10).join(parts)}
</div>
</body>
</html>
"""

if __name__ == "__main__":
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(html)
    print("mixture p_G:", dict(zip(ANSWERS, [round(m, 3) for m in MIX])))
