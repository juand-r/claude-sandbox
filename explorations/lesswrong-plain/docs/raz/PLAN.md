# Plan: all of Rationality: A–Z, in both editions

Request (user, 28 September 2026): extend the annotated and honest editions from 52 posts
to every post of *Rationality: A–Z*, with the same pipeline and quality. Put standards in
place first, run a pilot, then batches with subagents; the main session does the final
pass, review and writing, and logs every change. One book per edition. The 52 existing
posts are merged in.

## Scope (from the LessWrong API, `data/manifests/rationality_az.json`)

- 338 posts, about 461,000 words: 6 books, 26 sequences. 332 by Yudkowsky, 6 book
  introductions by Rob Bensinger.
- Already done: 45 of them. New: 293.
- 7 of our 52 are not in Rationality: A–Z (humans-are-not-automatically-strategic,
  toolbox-thinking-and-law-thinking, local-validity-as-a-key-to-sanity-and-civilization,
  diseased-thinking-dissolving-questions-about-disease, on-caring, strong-evidence-is-common,
  pr-is-corrosive). They go in a final part, "Beyond the Sequences", in their current order.
- Order: the collection's order, with book and sequence headings, in both editions.

## Process

1. [x] Commit what exists. Margin notes backed up without post text
       (`src/notes_backup.py`, `annotated/notes/`).
2. [x] Manifest (`src/fetch.py`, `rationality_az_manifest`); fetch all originals.
3. [x] Standards: `docs/STANDARDS.md` (specification), `docs/raz/AGENT_BRIEF.md`
       (agent instructions), `src/raz_check.py` (mechanical checks), `src/new_post.py`
       (skeletons), `src/edlog.py` (logged edits).
4. [x] Pilot: the 9 new posts of "Predictably Wrong", 3 agents × 3 posts. Editor's final
       pass on all 9. Revise the standards and brief from what the pilot shows.
5. [x] Book generators (`src/make_books.py`): `annotated/main.tex` and `honest/honest.tex` in collection order
       with book and sequence headings.
6. [ ] Batches: one sequence (or half of a long one) per wave, about 3 posts per agent.
       After each batch: editor's final pass, raz_check on every post, notes export,
       both builds, commit, push.
7. [ ] Last: a whole-book consistency pass (repeated criticisms, cross-references between
       posts, the honest edition's opening note).

## Logs

- `docs/raz/reports/<slug>.md`: each agent's report (sources, arithmetic, doubts).
- `docs/raz/changes/<batch>.md`: every edit in the editor's final pass, before and after.
- `docs/raz/review_log.md`: findings, decisions, and anything for the user.

## Status

| Batch | Sequence | Posts | Drafted | Final pass | Committed |
|---|---|---|---|---|---|
| pilot | Predictably Wrong | 9 | yes | yes | 43b43b5 |
| 1 | Fake Beliefs, Noticing Confusion, Mysterious Answers (rest of Book I) | 25 | yes | yes | fa1c1ba |
| 2a | Overly Convenient Excuses, Politics and Rationality, Against Rationalization, Against Doublethink | 33 | yes | yes | 98a40e5 |
| 2b | Seeing with Fresh Eyes, Death Spirals, Letting Go (rest of Book II) | 33 | yes | yes | 5320a09 |
| 3a | The Simple Math of Evolution, Fragile Purposes (Book III) | 24 | yes | yes | 4bf32c7 |
| 3b | A Human's Guide to Words (rest of Book III) | 26 | yes | yes | b4b7634 |
| 4a | Lawful Truth, Reductionism 101, Joy in the Merely Real (Book IV) | 31 | yes | yes | db86c92 |
