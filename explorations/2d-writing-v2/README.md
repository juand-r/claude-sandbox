# 2D Writing v2

Word grids that read as English both along rows and along columns. Successor
to `../2d-writing`. Here every row and every column is a real sentence that
occurs in a corpus: we collect a large set of short sentences and search
exactly for grids built from them, then rank the grids with a language model.

```
oh      but     you     can't
no      i       never   do
they    didn't  believe it
don't   ask     me      anymore
```

Across: Oh but you can't. No I never do. They didn't believe it. Don't ask me
anymore. Down: Oh no they don't. But I didn't ask. You never believe me. Can't
do it anymore.

Status: complete as of 2026-11-14. Results are in `docs/report.md` and `docs/gallery.md` (PDFs alongside). `PLAN.md` has the plan, `NOTES.md` the chronological findings.

## Setup

```bash
python3 -m venv venv
./venv/bin/pip install torch --index-url https://download.pytorch.org/whl/cpu
./venv/bin/pip install -r requirements.txt
gcc -O2 -o solver solver.c -lm
gcc -O2 -o fill fill.c
gcc -O2 -o ngram ngram.c
./venv/bin/python test_solver.py && ./venv/bin/python test_ngram.py
```

## Data (not in git, goes in `data/`)

```bash
cd data
curl -O https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/mono/en.txt.gz
mv en.txt.gz opensub_en.txt.gz
cd ..
./extract_opensub.sh                         # short sentences with counts
./venv/bin/python build_sentence_sets.py     # one file per sentence length, word counts
./venv/bin/python build_caps.py              # capitalized words (names)
```

## Pipeline

```bash
# 1. all 4x4 grids with 16 distinct words from sentences seen >= 20 times
./venv/bin/python run_exhaustive.py --rows 4 --cols 4 --min-count 20
# 2. language-model features for each grid (slow: ~250 grids/min on one core)
./venv/bin/python score_grids.py data/runs/<run>/grids.pkl 20 data/feat.pkl
# 3. best grids, with near-duplicates removed
./venv/bin/python gallery.py data/feat.pkl -n 20
```

## Files

| file | purpose |
|---|---|
| `sentences.py` | load and normalize sentence sets |
| `solver.c` | exact search, row-major fill over tries (the one used) |
| `fill.c` | exact search, most constrained line first (slower, kept as a check) |
| `ngram.c`, `ngrams.py` | search under n-gram rules instead of attested sentences (too loose, not used in results) |
| `search.py` | slow reference solver in Python, used by the tests |
| `grids.py` | Python front end for the C programs |
| `run_exhaustive.py` | resumable exhaustive runs split into parts |
| `lm.py`, `rank.py` | language-model scoring and ranking features |
| `score_grids.py`, `gallery.py` | score a set of grids, print the best |
| `surface_forms.py` | recover original punctuation of sentences from the corpus |
