# LessWrong in plain English

Rewrites of well-known LessWrong posts in plain modern English, keeping the
argument intact. Modeled on Jonathan Bennett's earlymoderntexts.com.
For personal reading.

## Layout
- `src/fetch.py` - fetches post lists and texts from the public LessWrong GraphQL API.
- `data/manifests/` - post lists (metadata only): `highlights.json` (the 50
  "Highlights from the Sequences") and `review_winners.json` (all Annual Review winners).
- `data/originals/` - fetched original texts. Not committed (authors' copyright).
- `rewrites/` - the plain-English rewrites. Not committed for now (this repo is public).
- `annotated/` - LaTeX edition: original text, commentary in the margin. Build: `cd annotated && latexmk -pdf -outdir=build main.tex`.
- `src/check_verbatim.py` - confirms the annotated main text matches the original.
- `docs/STYLE.md` - rewriting rules. `docs/PLAN.md` - plan. `docs/NOTES.md` - log.

## Run
```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python src/fetch.py manifests
.venv/bin/python src/fetch.py posts highlights
```
