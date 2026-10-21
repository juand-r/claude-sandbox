"""Compact version of the paper's Table 2 (segmentation examples) for the lower left of the poster.

Six words not already shown in the cartoon, four of the six tokenizers (WordPiece and Morfessor
dropped for space: WordPiece splits like BPE here, Morfessor keeps nearly every word whole).
Every cell is copied from Table 2. Pieces are drawn as neutral chips; no colour judgement.

Size: 965 x 419 px = 724 x 314 pt, the space under "What we did" in the user's Keynote layout.

Run:  python make_examples.py  -> figures/examples.html
Then: node render_figure.js figures/examples.html  -> .pdf (vector) and .png (transparent)
"""
from pathlib import Path

OUT = Path(__file__).parent / "figures" / "examples.html"
W, H = 965, 419
INK, MUTED, BLUE, RULE = "#14161A", "#4A4F57", "#2F5D9B", "#C9CDD3"

COLUMNS = ["Ours", "BPE", "Unigram", "MorphPiece (raw)"]
# word -> segmentations in COLUMNS order (Table 2)
ROWS = [
    ("nutritious",    ["nutrit ous",       "nutritious",     "nutritio u s",   "nutrition ous"]),
    ("crier",         ["cry er",           "crier",          "crie r",         "cry er"]),
    ("running",       ["run ing",          "running",        "running",        "run er ing"]),
    ("werewolf",      ["werewolf",         "werewolf",       "werewolf",       "were wolf"]),
    ("prehistoric",   ["pre history ic",   "prehistoric",    "pre historic",   "pre history ic"]),
    ("nationalistic", ["nation al ist ic", "national istic", "national istic", "nation al ist ic"]),
]
WORD_W, COL_WS = 175, (215, 180, 180, 215)   # px; 175 + 790 = 965
HEAD_H, ROW_H = 50, 61                   # 50 + 6 * 61 = 416


def cell(seg):
    return "".join(f'<span class="chip">{p}</span>' for p in seg.split())


head = (f'<div class="row head" style="height: {HEAD_H}px"><div class="w"></div>'
        + "".join(f'<div class="c{" ours" if i == 0 else ""}" style="width: {COL_WS[i]}px">{c}</div>' for i, c in enumerate(COLUMNS)) + "</div>")
body = "".join(
    f'<div class="row" style="height: {ROW_H}px"><div class="w">{w}</div>'
    + "".join(f'<div class="c{" ours" if i == 0 else ""}" style="width: {COL_WS[i]}px">{cell(s)}</div>' for i, s in enumerate(segs)) + "</div>"
    for w, segs in ROWS)

page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Segmentation examples (Table 2)</title>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;700&amp;display=swap" rel="stylesheet">
<style>
html, body {{ margin: 0; background: transparent }}
#figure {{ position: relative; width: {W}px; height: {H}px; font-family: Archivo, 'Helvetica Neue', sans-serif; color: {INK} }}
.row {{ display: flex; align-items: center; box-sizing: border-box; border-bottom: 2px solid {RULE} }}
.row:last-child {{ border-bottom: 0 }}
.head {{ border-bottom: 3px solid {INK}; font-size: 24px; font-weight: 700 }}
.w {{ width: {WORD_W}px; flex: none; font-size: 26px; color: {MUTED} }}
.c {{ flex: none; display: flex; gap: 4px; flex-wrap: nowrap }}
.head .c.ours {{ color: {BLUE} }}
.chip {{ display: inline-block; font-size: 22px; line-height: 1; padding: 7px 4px; border-radius: 8px; border: 2px solid #9AA1AA; background: #FFFFFF; white-space: nowrap }}
.c.ours .chip {{ border-color: {BLUE} }}
</style>
</head>
<body>
<div id="figure">
{head}
{body}
</div>
</body>
</html>
"""

if __name__ == "__main__":
    assert WORD_W + sum(COL_WS) == W and len(COL_WS) == len(COLUMNS)
    assert all(len(s) == len(COLUMNS) for _, s in ROWS)
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(page)
    print("wrote", OUT)
