# LessWrong in plain English

Rewrites of well-known LessWrong posts in plain modern English, keeping the
argument intact. Modeled on Jonathan Bennett's earlymoderntexts.com.
For personal reading.

## Layout
- `src/fetch.py` - fetches post lists and texts from the public LessWrong GraphQL API.
- `data/manifests/` - post lists (metadata only): `highlights.json` (the 50
  "Highlights from the Sequences"), `review_winners.json` (all Annual Review winners) and
  `rationality_az.json` (the 338 posts of Rationality: A-Z, in reading order).
- `data/originals/` - fetched original texts. Not committed (authors' copyright).
- `rewrites/` - the plain-English rewrites. Not committed for now (this repo is public).
- `annotated/` - LaTeX edition: original text, commentary in the margin. Build: `cd annotated && latexmk -pdf -outdir=build main.tex`.
- `src/check_verbatim.py` - confirms the annotated main text matches the original.
- `src/notes_backup.py` - backs up the margin notes (`annotated/notes/*.json`, committed) without the
  post text, and restores `annotated/posts/` from them. Run `export` and `check` before every commit.
- `docs/STYLE.md` - rewriting rules. `docs/PLAN.md` - plan. `docs/NOTES.md` - log.

## Run
```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python src/fetch.py manifests
.venv/bin/python src/fetch.py posts highlights
```
