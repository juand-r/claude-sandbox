# 2D Writing v2

Word grids that read as English both along rows and along columns. Successor
to `../2d-writing`. Here every row and every column is a real, attested
sentence: we collect a large set of short sentences and search exactly for
grids built from them.

```
what  would you   take
did   tom   see   this
i     like  that  stuff
do    it    right away
```

Status: in progress. See `PLAN.md` for the plan and `NOTES.md` for findings.

## Setup

```bash
python3 -m venv venv && ./venv/bin/pip install torch --index-url https://download.pytorch.org/whl/cpu
./venv/bin/pip install -r requirements.txt
gcc -O2 -o solver solver.c -lm
gcc -O2 -o fill fill.c
./venv/bin/python test_solver.py
```

Data goes in `data/` (not in git). Sources and download commands are in
`NOTES.md` and `extract_opensub.sh`.
