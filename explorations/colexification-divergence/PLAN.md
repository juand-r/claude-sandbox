# Plan: Colexification-Forced Information Divergence

Started 2 August 2026, picking up from a handoff (see `inherited/HANDOFF.md`).

## The core idea (inherited, unchanged)

If language A uses one word for concepts X and Y, and language B uses two, then a
B-speaker rendering A-content must commit to X or Y. The commitment is information
that was not in the source, and it is forced by lexical structure rather than
editorial choice. CLICS4 catalogues where these splits occur across ~3400 language
varieties, so it can predict in advance where forced divergence should arise.

## Audit of the inherited state

Done before writing this plan, so the plan rests on verified facts and not on the
handoff's own summary of itself.

### Verified correct

- The headline family counts in `inherited/README.md` match CLICS4 exactly:
  LEG/FOOT 100 families, FLESH/MEAT 105, DO/MAKE 76, BLUE/GREEN 70, MOON/MONTH 60,
  WOMAN/WIFE 59, MOUNTAIN/HILL 84, WOOD/TREE 58.
- The claim that CLICS detects colexification on the `Segments` column (IPA), not
  `Form` (orthographic), matches the CLICS4 source.

### Verified broken

- **The concept-pair join fails silently.** `inherited/src/extract_v2.py` and
  `extract_asymmetries.py` join `forms.csv` to `colexifications.csv` on concept
  identifiers, but `forms.Parameter_ID` is a lowercase slug (`leg`) while
  `colexifications.Source_Concept` is an uppercase name (`LEG`). Measured overlap
  between the two vocabularies: **0 of 1730 concepts**. Every row in
  `inherited/data/*.tsv` therefore carries `family_count=0, language_count=0`, and
  the ranking those files claim to present is not a ranking at all — it is
  alphabetical order over a constant.
- **Homophony dominates the English-only output.** The top of
  `inherited/data/english_only.tsv` is `yoke/yolk`, `weak/week`, `son/sun`,
  `sow/sew`, `sea/see`. These are accidental phonological collisions, not semantic
  associations. The handoff lists the homophone filter as a minor unfinished item;
  the data says it is the difference between a usable table and an unusable one.
- Minor: the handoff gives SKIN/BARK as 53 families; CLICS4 says 62. (53 is
  HEAR/LISTEN's count, so this looks like a transcription slip.)

### Cannot be verified

- The 20 sentences in `inherited/data/test_sentences.json` are hand-collected and
  their sources are named only in prose ("Reverso Context, Linguee, Cornell Russian
  Lexical Database"). There are no per-sentence provenance records, so I cannot
  check any individual sentence against its claimed origin.
- The `disambiguation` field (none / weak_X / strong_X) is a single annotator's
  judgement with no second pass and no adjudication.

## Environment facts

- CLICS4 clones cleanly from GitHub; full CLDF data is in `vendor/clics4` (390 MB,
  gitignored). Re-fetch with `src/setup_clics4.sh`.
- **No `ANTHROPIC_API_KEY` in this environment.** `inherited/src/test_haiku.py`
  cannot run as written.
- `OPENAI_API_KEY` is set and works, with access to the GPT-4o, GPT-4.1, GPT-5.x,
  and o3/o4 families. Any LLM experiment run here is an OpenAI experiment.

## The design problem I want to raise before building on Phase 3

The inherited experiment sends each sentence to a model five times and asks whether
the same word comes back each time. It calls agreement "consistent" and variation
"inconsistent", with the implication that consistency is the good outcome.

That reading does not survive contact with the premise of the project. If the
source sentence is genuinely underspecified, a model that answers "leg" five times
out of five has committed hard to information the source did not contain. A model
that splits three-two has, if anything, represented the underdetermination better.
Self-consistency under resampling measures decoding entropy. It does not measure
whether the model tracks what the source did and did not say.

The measurement the premise actually calls for is **calibration to source
ambiguity**: the choice distribution should be near-uniform where context
disambiguates nothing and near-deterministic where context disambiguates strongly.
That quantity uses the `disambiguation` annotation already in the test set, it is
falsifiable, and "consistency" falls out of it as a special case. This is a change
in what we measure, not merely how we describe it, so it is question 2 to the user
rather than something I adopt on my own.

## Phases

Status markers: `[ ]` not started, `[~]` in progress, `[x]` done, `[!]` blocked or
abandoned (with a note).

### Phase 0 — Project setup
- [x] Copy inherited materials verbatim into `inherited/` (never edited in place)
- [x] Clone CLICS4 into `vendor/`, gitignore it
- [x] Audit the inherited claims against the data (above)
- [x] Write this plan
- [ ] Commit the starting state before changing anything

### Phase 1 — Rebuild the CLICS extraction so its output is trustworthy
- [ ] Fix the concept join (normalise slug vs. name across the two tables)
- [ ] Implement the homophone filter: within a language, flag pairs whose
      `Segments` match but whose `Form` differs, since those are candidates for
      accidental homophony rather than shared meaning
- [ ] Add the corroboration test the design doc already proposed: a pair attested
      in many unrelated families is unlikely to be coincidence, so global family
      count is itself evidence against homophony
- [ ] Generalise from hardcoded English/Spanish to an arbitrary language pair
- [ ] Regenerate the asymmetry tables and compare against `inherited/data/*.tsv`,
      recording what the fix changes

### Phase 2 — Test set
Blocked on question 3 (corpus choice). Sub-steps depend on the answer.
- [ ] Decide corpus: Tatoeba (small, clean, aligned) vs. OpenSubtitles (large,
      noisy, colloquial)
- [ ] Extract candidate sentences containing the colexifying word
- [ ] Annotate degree of disambiguation, with provenance recorded per sentence
- [ ] Keep the inherited 20 sentences as a separate labelled subset, not merged
      silently into the new set

### Phase 3 — LLM measurement
Blocked on question 2 (what to measure).
- [ ] Port the runner to the OpenAI API
- [ ] Implement the agreed metric
- [ ] Run, with raw responses saved for re-analysis
- [ ] Report

### Phase 4 — Write-up
- [ ] Connect to X-PARADE's taxonomy (same / new / inferable)
- [ ] Full-exposition report per the repository's report guidelines

## Open questions for the user

1. Priority for this session.
2. Consistency vs. calibration as the Phase 3 metric (see above).
3. Tatoeba vs. OpenSubtitles for Phase 2.
4. Paper framing, which decides what to prioritise after Phase 1.

## Log

- **2 Aug 2026** — Set up, audited inherited work, found and confirmed the join
  bug. Wrote this plan. Awaiting answers on the four questions above.
