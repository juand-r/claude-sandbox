"""Two Method figures for the user's Keynote layout (row under the existing Method content).

curation.html : what hand curation changed relative to raw MorphyNet (paper Sec. 4.3 and 5.1):
                of 28,571 explicit decisions, 4,961 splits added, 3,933 re-segmented, 1,114 rejected.
quality.html  : quality checks. LLM audit of 7,600 further MorphyNet words (Sec. 4.3): ~11% errors in a
                1,000-word sample, ~5% in a fresh 1,200-word sample after fixes. MorphoLex comparison
                on 68,617 words (Appendix H, Table 8).

Each is 965 px wide (= 724 pt, one Method column).
Run:  python make_method_extras.py  -> figures/curation.html, figures/quality.html
Then: node render_figure.js figures/curation.html (and quality.html)
"""
from pathlib import Path

FIG = Path(__file__).parent / "figures"
INK, MUTED, BLUE, GREEN, RED, GREY = "#14161A", "#4A4F57", "#2F5D9B", "#2E8B57", "#C8483A", "#9AA1AA"
W = 965

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;700&amp;display=swap" rel="stylesheet">
<style>
html, body {{ margin: 0; background: transparent }}
#figure {{ position: relative; width: {w}px; height: {h}px; font-family: Archivo, 'Helvetica Neue', sans-serif; color: """ + INK + """ }}
#figure div {{ position: absolute; box-sizing: border-box }}
{css}
</style>
</head>
<body>
<div id="figure">
{body}
</div>
</body>
</html>
"""

# ---------------------------------------------------------------- curation
CURATION = [  # label, count, colour, example
    ("Added", 4961, GREEN, "splits MorphyNet does not list"),
    ("Re-segmented", 3933, BLUE, "kingdom: kin + ing + dom → king + dom"),
    ("Rejected", 1114, RED, "business: busy + ness → kept whole"),
]
C_H, C_ROW = 200, 64                     # 3 rows of 64 px, last example line ends at 194
C_LABEL_W, C_BAR_X, C_BAR_MAX = 236, 246, 320
C_COUNT_X = C_BAR_X + C_BAR_MAX + 14


def curation_page():
    top = max(c for _, c, _, _ in CURATION)
    rows = []
    for i, (label, n, colour, ex) in enumerate(CURATION):
        y = i * C_ROW + 6
        w = n / top * C_BAR_MAX
        rows.append(
            f'<div class="lab" style="top: {y}px">{label}</div>'
            f'<div class="bar" style="top: {y + 6}px; left: {C_BAR_X}px; width: {w:.0f}px; background: {colour}"></div>'
            f'<div class="num" style="top: {y}px; left: {C_BAR_X + w + 12:.0f}px">{n:,}</div>'
            f'<div class="ex" style="top: {y + 34}px; left: {C_BAR_X}px">{ex}</div>')
    css = (f".lab {{ left: 0; width: {C_LABEL_W - 14}px; text-align: right; font-size: 26px; font-weight: 700; line-height: 34px }}\n"
           ".bar { height: 22px; border-radius: 4px }\n"
           ".num { font-size: 26px; font-weight: 700; line-height: 34px }\n"
           f".ex {{ width: {W - C_BAR_X}px; font-size: 22px; line-height: 26px; color: {MUTED} }}")
    return HEAD.format(title="What curation changed", w=W, h=C_H, css=css, body="\n".join(rows))


# ---------------------------------------------------------------- quality
MORPHOLEX = [  # share of 68,617 words (Table 8), colour, label shown under the bar or None
    (25.5 + 24.4, GREEN, "agree 49.9%"),
    (37.8, "#8FA6C8", "MorphoLex splits further 37.8%: Latin/Greek roots we keep whole"),
    (1.0, RED, None),
    (3.7 + 7.6, "#D5D9DE", None),
]
Q_H = 262                                # last note line ends at 255
BAR_Y, BAR_H = 128, 34


def quality_page():
    body = [
        '<div class="lab" style="top: 0">LLM audit</div>',
        '<div class="txt" style="top: 0">error rate in a sample: <b>~11%</b> &nbsp;→&nbsp; <b>~5%</b> after fixes</div>',
        '<div class="sub" style="top: 36px">7,600 further MorphyNet words; samples of 1,000 and 1,200 words</div>',
        f'<div class="lab" style="top: {BAR_Y - 40}px">MorphoLex</div>',
        f'<div class="txt" style="top: {BAR_Y - 40}px">68,617 expert-segmented words</div>',
    ]
    x = 0.0
    for share, colour, _ in MORPHOLEX:
        w = share / 100 * W
        body.append(f'<div style="left: {x:.1f}px; top: {BAR_Y}px; width: {w:.1f}px; height: {BAR_H}px; background: {colour}"></div>')
        x += w
    body.append(f'<div class="sub" style="top: {BAR_Y + BAR_H + 8}px; left: 0; width: 300px">agree <b>49.9%</b></div>')
    left2 = (25.5 + 24.4) / 100 * W
    body.append(f'<div class="sub" style="top: {BAR_Y + BAR_H + 8}px; left: {left2:.0f}px; width: {W - left2:.0f}px">'
                'MorphoLex splits further <b>37.8%</b><br>(Latin/Greek roots we keep whole)</div>')
    body.append(f'<div class="sub" style="top: {BAR_Y + BAR_H + 66}px; left: 0; width: {W}px">'
                f'<span class="key" style="background: {RED}"></span>we split further <b>1.0%</b> &nbsp; '
                f'<span class="key" style="background: #D5D9DE"></span>other <b>11.3%</b> (spelling conventions, words we cannot analyze)</div>')
    css = (".lab { left: 0; width: 150px; font-size: 26px; font-weight: 700; line-height: 34px }\n"
           ".txt { left: 160px; width: 805px; font-size: 26px; line-height: 34px }\n"
           f".sub {{ left: 160px; width: 805px; font-size: 22px; line-height: 27px; color: {MUTED} }}\n"
           f".sub b {{ color: {INK} }}\n"
           ".key { display: inline-block; width: 16px; height: 16px; margin-right: 6px; vertical-align: -1px }")
    return HEAD.format(title="Quality checks", w=W, h=Q_H, css=css, body="\n".join(body))


if __name__ == "__main__":
    assert abs(sum(s for s, _, _ in MORPHOLEX) - 100.0) < 0.05
    FIG.mkdir(exist_ok=True)
    (FIG / "curation.html").write_text(curation_page())
    (FIG / "quality.html").write_text(quality_page())
    print("wrote figures/curation.html, figures/quality.html")
