# Colexification-Forced Information Divergence

Uses CLICS4 to predict where one language forces a speaker to commit to a
distinction another language leaves open, then tests whether LLMs handle those
points sensibly.

Picked up from a predecessor's handoff on 2 August 2026. Their materials are in
`inherited/`, kept verbatim; `PLAN.md` records what I audited, what held up, and
what did not.

## The idea in one paragraph

Russian `noga` covers both *leg* and *foot*. A Russian speaker who says "my noga
hurts" has not said where the pain is. An English translator must pick one, and the
pick adds information the source never carried. The same happens with Spanish
`mujer` (woman / wife) and Japanese `kiku` (hear / listen). CLICS4 catalogues these
patterns across ~3400 language varieties, so for any language pair it can say in
advance where such forced commitments should arise.

## Layout

```
.
├── PLAN.md          # plan, audit of the inherited work, and running log
├── src/             # this project's code
├── data/            # this project's outputs
├── notes/           # working notes
├── inherited/       # predecessor's materials, unmodified
└── vendor/clics4/   # CLICS4 database (gitignored, ~390 MB)
```

## Setup

```bash
src/setup_clics4.sh     # clone CLICS4 and unzip forms.csv / colexifications.csv
```

Python 3.10+, standard library only for the extraction step.

## Status

Phase 0 (setup and audit) done. Phase 1 (rebuilding the extraction) is next; the
inherited extraction output is unusable because of a silent join failure documented
in `PLAN.md`. Later phases are waiting on decisions listed at the end of that file.
