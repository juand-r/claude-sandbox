"""Generate the poster's two SVG charts from numbers copied out of the paper.

Source: arXiv 2607.02668v1, Table 2 (main results) and Table 5 (validator).
Run:  python make_charts.py  -> writes chart_results.svg and chart_validator.svg
The SVG markup is pasted into the poster artboard (Main.dc.html).
"""
from pathlib import Path

OUT = Path(__file__).parent

# Colors (validated with the dataviz palette checker: blue/orange pass CVD checks).
INK, MUTED, GRID, SURFACE = "#14161A", "#4A4F57", "#D3D7DC", "#F6F7F5"
GREY, ORANGE = "#7D838C", "#D2601A"
FONT = "Archivo, 'Helvetica Neue', sans-serif"

SETTINGS = [  # (task, model) in Table 2 column order
    ("IFEval", "Gemma-2-9b-it"), ("IFEval", "Qwen-3.5-9B"),
    ("HumanEval", "Gemma-4-31b-it"), ("HumanEval", "Qwen-3.5-9B"),
    ("Hyponymy", "Gemma-2-9b-it"), ("Hyponymy", "Qwen-3.5-9B"),
]

# Table 2: (ROC_G, rho) per setting, in SETTINGS order.
TABLE2 = {
    "Base":           [(78.2, 35.5), (69.3, 21.5), (72.9, 22.4), (65.7, 30.4), (81.2, 48.0), (73.5, 42.9)],
    "SFT":            [(74.4, 29.5), (73.1, 24.1), (84.5, 28.5), (94.1, 56.3), (88.1, 64.0), (82.6, 48.6)],
    "Consistency FT": [(58.7, 0.8), (69.8, 22.4), (74.9, 49.0), (92.6, 53.5), (85.3, 50.8), (80.1, 56.6)],
    "RankAlign":      [(74.9, 29.9), (75.4, 32.8), (86.9, 40.9), (90.2, 69.5), (91.6, 75.2), (88.2, 70.4)],
    "FLORA-PMI":      [(85.1, 62.8), (79.6, 43.3), (92.2, 66.8), (83.2, 58.9), (92.5, 73.8), (87.3, 69.4)],
    "FLORA-Neg":      [(60.8, 34.4), (66.0, 44.7), (94.2, 76.3), (88.9, 68.5), (92.3, 72.2), (88.2, 69.4)],
}
PRIOR = ["SFT", "Consistency FT", "RankAlign"]
FLORA = ["FLORA-PMI", "FLORA-Neg"]

# Table 5: validator accuracy Acc_V per setting.
ACC_V = {
    "Base":      [59.7, 70.8, 71.4, 65.3, 87.1, 87.9],
    "FLORA-PMI": [63.6, 73.6, 85.8, 76.4, 84.6, 86.8],
    "FLORA-Neg": [67.5, 71.8, 88.3, 78.3, 84.9, 87.3],
}


def best(methods, i, metric):
    """Best value among `methods` for setting i; metric 0 = ROC_G, 1 = rho (as in Table 2)."""
    return max(TABLE2[m][i][metric] for m in methods)


def num(v, fmt="+.1f"):
    """Format a number with a typographic minus sign."""
    return format(v, fmt).replace("-", "\u2212")


def text(x, y, s, size=26, fill=INK, anchor="start", weight=400):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" '
            f'text-anchor="{anchor}" font-weight="{weight}">{s}</text>')


def results_chart():
    W, LABEL_W, ROW_H, TOP = 1072, 280, 116, 70
    panels = [  # (title, metric index, domain, ticks, x0, x1)
        ("Generator AUROC", 0, (60, 100), [60, 70, 80, 90, 100], 310, 646),
        ("G–V correlation ρ ×100", 1, (20, 80), [20, 40, 60, 80], 736, 1048),
    ]
    n = len(SETTINGS)
    bottom = TOP + n * ROW_H
    H = bottom + 56
    out = [f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
           f'aria-label="Dot plot of generator AUROC and generator-validator correlation for six settings" '
           f'style="display: block; font-family: {FONT}">']
    for title, metric, (lo, hi), ticks, x0, x1 in panels:
        sx = lambda v: x0 + (v - lo) / (hi - lo) * (x1 - x0)
        out.append(text((x0 + x1) / 2, 34, title, 28, INK, "middle", 700))
        for t in ticks:
            out.append(f'<line x1="{sx(t):.1f}" y1="{TOP}" x2="{sx(t):.1f}" y2="{bottom}" stroke="{GRID}" stroke-width="2"/>')
            out.append(text(sx(t), bottom + 40, t, 26, MUTED, "middle"))
        for i in range(n):
            cy = TOP + (i + 0.5) * ROW_H
            base = TABLE2["Base"][i][metric]
            prior, flora = best(PRIOR, i, metric), best(FLORA, i, metric)
            lo_v, hi_v = min(base, prior, flora), max(base, prior, flora)
            out.append(f'<line x1="{sx(lo_v):.1f}" y1="{cy}" x2="{sx(hi_v):.1f}" y2="{cy}" stroke="{GRID}" stroke-width="4"/>')
            out.append(f'<circle cx="{sx(base):.1f}" cy="{cy}" r="10" fill="{SURFACE}" stroke="{GREY}" stroke-width="4"/>')
            out.append(f'<circle cx="{sx(prior):.1f}" cy="{cy}" r="12" fill="{GREY}" stroke="{SURFACE}" stroke-width="3"/>')
            out.append(f'<circle cx="{sx(flora):.1f}" cy="{cy}" r="14" fill="{ORANGE}" stroke="{SURFACE}" stroke-width="3"/>')
            out.append(text(sx(flora), cy - 24, f"{flora:.1f}", 26, INK, "middle", 700))
            out.append(text(sx(prior), cy + 42, f"{prior:.1f}", 24, MUTED, "middle"))
    for i, (task, model) in enumerate(SETTINGS):
        cy = TOP + (i + 0.5) * ROW_H
        out.append(text(0, cy - 4, task, 30, INK, weight=700))
        out.append(text(0, cy + 30, model, 26, MUTED))
        if i in (2, 4):  # separate the three tasks
            y = TOP + i * ROW_H
            out.append(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="{GRID}" stroke-width="2" stroke-dasharray="6 8"/>')
    out.append("</svg>")
    return "\n".join(out)


def validator_chart():
    W, ROW_H, TOP = 1072, 66, 10
    lo, hi, x0, x1 = -5, 20, 380, 900
    sx = lambda v: x0 + (v - lo) / (hi - lo) * (x1 - x0)
    n = len(SETTINGS)
    bottom = TOP + n * ROW_H
    H = bottom + 56
    out = [f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
           f'aria-label="Change in validator accuracy after FLORA training, six settings" '
           f'style="display: block; font-family: {FONT}">']
    for t in (-5, 0, 5, 10, 15, 20):
        w = 3 if t == 0 else 2
        c = MUTED if t == 0 else GRID
        out.append(f'<line x1="{sx(t):.1f}" y1="{TOP}" x2="{sx(t):.1f}" y2="{bottom}" stroke="{c}" stroke-width="{w}"/>')
        out.append(text(sx(t), bottom + 40, num(t, "+d") if t else "0", 26, MUTED, "middle"))
    for i, (task, model) in enumerate(SETTINGS):
        cy = TOP + (i + 0.5) * ROW_H
        deltas = [ACC_V[m][i] - ACC_V["Base"][i] for m in FLORA]
        a, b = min(deltas), max(deltas)
        xa, xb = sx(a), sx(b)
        out.append(f'<rect x="{xa - 9:.1f}" y="{cy - 9}" width="{xb - xa + 18:.1f}" height="18" rx="9" fill="{ORANGE}"/>')
        label = f"{num(a)} to {num(b)}"
        out.append(text(max(xb, sx(0)) + 22, cy + 9, label, 26, INK))
        out.append(text(0, cy + 9, f"<tspan font-weight=\"700\">{task}</tspan> {model}", 26, INK))
    out.append("</svg>")
    return "\n".join(out)


if __name__ == "__main__":
    (OUT / "chart_results.svg").write_text(results_chart())
    (OUT / "chart_validator.svg").write_text(validator_chart())
    for i, s in enumerate(SETTINGS):
        print(s, "ROC prior/FLORA", best(PRIOR, i, 0), best(FLORA, i, 0),
              "| rho prior/FLORA", best(PRIOR, i, 1), best(FLORA, i, 1),
              "| dAccV", [round(ACC_V[m][i] - ACC_V["Base"][i], 1) for m in FLORA])
