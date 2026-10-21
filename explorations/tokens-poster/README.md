# Tokens of Meaning poster

A0 portrait poster (EMNLP 2026 / BabyLM workshop) for "Tokens of Meaning: Semantically-Informed Morphological Tokenization in Low-Resource Language Modeling". Style and layout follow the final FLORA poster (`../flora-poster`, the user's v7).

## Files

- `poster-a0.html`: the poster, 3179 × 4494 px (A0 at 96 px/in).
- `poster-a0.pptx`: editable version for Keynote (built from the HTML).
- `poster-a0-preview.png`: render of the HTML.
- `figures/`: each figure as HTML source, vector PDF and transparent PNG.
  - `cartoon` (band), `pooling` (Overview), `decision` and `normalize` (Method), `results` (Results).
- `assets/qr-code.png`: QR code for github.com/juand-r/morpheus-tokenizer.
- `NOTES.md`: plan, layout decisions, and the source in the paper for every number.

## How to rebuild

```
npm install
python3 make_cartoon.py && python3 make_chart.py
for f in cartoon pooling decision normalize results; do node render_figure.js figures/$f.html; done
node check_layout.js      # preview PNG + overflow report
node build_pptx.js        # poster-a0.pptx
```

Needs Playwright with Chromium (global install). The poster loads Archivo from `assets/fonts/` (full font; the Google Fonts web subset lacks the ∙ used in the title). Install Archivo locally for Keynote and LibreOffice.
