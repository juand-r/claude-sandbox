"""Cartoon band for the poster: the same five words under three tokenizers.

Segmentations are copied from Table 2 of the paper (BPE, MorphPiece on raw MorphyNet, Ours).
Chip colours are our reading of the paper's argument: green = a meaningful morpheme,
red = a piece that misleads (no meaning, or the wrong meaning), white = word kept whole.

Run:  python make_cartoon.py  -> figures/cartoon.html
Then: node render_figure.js figures/cartoon.html  -> .pdf (vector) and .png (transparent)
"""
from pathlib import Path

OUT = Path(__file__).parent / "figures" / "cartoon.html"
W, H = 2987, 860                        # px on the 3179 px wide A0 artboard (96 px/in)
MARGIN = 6                              # keeps outer strokes from being clipped

INK, MUTED, GREEN, RED, BLUE = "#14161A", "#4A4F57", "#2E8B57", "#C8483A", "#2F5D9B"
GREEN_BG, RED_BG = "#E3F2E8", "#FBE4E1"
FONT = "Archivo, 'Helvetica Neue', sans-serif"

WORDS = ["unhappiness", "happiness", "business", "adder", "singleton"]
WORD_NOTES = {"adder": "a snake"}

# Each entry: list of (piece, kind) with kind in {"good", "bad", "whole"}.
PANELS = [
    dict(title="Statistical (e.g., BPE)", sub="splits to compress text",
         rows=[[("unhappiness", "whole")], [("happiness", "whole")], [("business", "whole")],
               [("ad", "bad"), ("der", "bad")], [("sing", "bad"), ("leton", "bad")]],
         caption=["Pieces ignore meaning, and", "related words share nothing"]),
    dict(title="Morphology, uncurated", sub="MorphPiece on raw MorphyNet",
         rows=[[("un", "good"), ("hap", "bad"), ("y", "bad"), ("ness", "good")],
               [("hap", "bad"), ("y", "bad"), ("ness", "good")],
               [("busy", "bad"), ("ness", "bad")],
               [("add", "bad"), ("er", "bad")], [("single", "bad"), ("ton", "bad")]],
         caption=["Real morphemes, wrong splits:", "business is not busy + ness"]),
    dict(title="Ours: morphology + meaning", sub="hand-curated over MorphyNet",
         rows=[[("un", "good"), ("happy", "shared"), ("ness", "good")],
               [("happy", "shared"), ("ness", "good")],
               [("business", "whole")], [("adder", "whole")], [("singleton", "whole")]],
         caption=["Split only when the pieces", "keep the word’s meaning"]),
]
PANEL_W, PANEL_GAP = 935, 91            # 3 * 935 + 2 * 91 = 2987


def chip(piece, kind):
    return f'<span class="chip {kind}">{piece}</span>'


def panel_html(k, P):
    rows = []
    for word, pieces in zip(WORDS, P["rows"]):
        note = f'<span class="wnote">{WORD_NOTES[word]}</span>' if word in WORD_NOTES else ""
        rows.append(f'<div class="row"><div class="word">{word}{note}</div>'
                    f'<div class="chips">{"".join(chip(p, kind) for p, kind in pieces)}</div></div>')
    shared = ('<div class="shared-note">same token: <b>happy</b></div>' if k == 2 else "")
    title_color = BLUE if k == 2 else INK
    return f"""
<div class="panel" style="left: {k * (PANEL_W + PANEL_GAP)}px">
  <div class="ptitle" style="color: {title_color}">{P['title']}</div>
  <div class="psub">{P['sub']}</div>
  <div class="card">{''.join(rows)}{shared}</div>
  <div class="caption">{'<br>'.join(P['caption'])}</div>
</div>"""


LEGEND = (f'<div class="legend">{chip("meaningful morpheme", "good")}{chip("misleading piece", "bad")}'
          f'{chip("kept whole", "whole")}</div>')

page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Tokenizer cartoon</title>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;700&amp;display=swap" rel="stylesheet">
<style>
html, body {{ margin: 0; background: transparent }}
#figure {{ position: relative; width: {W + 2 * MARGIN}px; height: {H + 2 * MARGIN}px; font-family: {FONT}; color: {INK} }}
.canvas {{ position: absolute; left: {MARGIN}px; top: {MARGIN}px; width: {W}px; height: {H}px }}
.panel {{ position: absolute; top: 0; width: {PANEL_W}px }}
.ptitle {{ font-size: 44px; font-weight: 700; line-height: 1.1; display: flex; gap: 18px; align-items: center; justify-content: center }}
.psub {{ font-size: 30px; color: {MUTED}; text-align: center; margin-top: 8px; height: 40px }}
.card {{ position: relative; margin-top: 22px; background: #FFFFFF; border: 4px solid {INK}; border-radius: 26px;
         padding: 26px 30px; display: flex; flex-direction: column; gap: 18px; height: 524px; box-sizing: border-box }}
.row {{ display: flex; align-items: center; gap: 26px; height: 78px }}
.word {{ width: 250px; flex: none; text-align: right; font-size: 32px; color: {MUTED}; line-height: 1.1 }}
.wnote {{ display: block; font-size: 23px; color: {MUTED} }}
.chips {{ display: flex; gap: 10px }}
.chip {{ display: inline-block; font-size: 36px; line-height: 1; padding: 14px 16px; border-radius: 12px; border: 3px solid; white-space: nowrap }}
.chip.good {{ background: {GREEN_BG}; border-color: {GREEN}; color: {INK} }}
.chip.shared {{ background: {GREEN_BG}; border: 5px solid {BLUE}; padding: 12px 14px; color: {INK}; font-weight: 700 }}
.chip.bad {{ background: {RED_BG}; border-color: {RED}; color: {INK} }}
.chip.whole {{ background: #FFFFFF; border-color: #9AA1AA; color: {INK} }}
.shared-note {{ position: absolute; right: 30px; top: 66px; font-size: 26px; color: {BLUE}; text-align: right; line-height: 1.2 }}
.caption {{ margin-top: 24px; font-size: 34px; font-weight: 700; text-align: center; line-height: 1.25 }}
.legend {{ position: absolute; left: 0; bottom: 0; width: {W}px; display: flex; gap: 22px; align-items: center; justify-content: center }}
.legend .chip {{ font-size: 26px; padding: 8px 12px; border-width: 3px }}
</style>
</head>
<body>
<div id="figure"><div class="canvas">
{''.join(panel_html(k, P) for k, P in enumerate(PANELS))}
{LEGEND}
</div></div>
</body>
</html>
"""

if __name__ == "__main__":
    for P in PANELS:
        assert len(P["rows"]) == len(WORDS)
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(page)
    print("wrote", OUT)
