# Phase 1: what it takes to get a trustworthy asymmetry table out of CLICS4

Working notes from rebuilding the extraction, 2 August 2026.

## Summary

Three separate defects stand between CLICS4's raw tables and a list of concept
pairs that one language colexifies and another does not. Two are fixed here; the
third is characterised but not fixable from the data alone.

| # | Defect | Effect if unhandled | Status |
|---|--------|---------------------|--------|
| 1 | Concept identifiers differ between the two tables | All family counts zero; output unranked | Fixed |
| 2 | `Form` is orthographic in some varieties, IPA in others | Homophones pass as colexifications | Fixed |
| 3 | Multi-alternative source cells expanded across concepts | Colexifications manufactured wholesale | Partly fixed |

## Defect 1: the silent join failure

`forms.csv` identifies concepts by a lowercase slug in `Parameter_ID` (`leg`).
`colexifications.csv` identifies them by an uppercase name in `Source_Concept`
and `Target_Concept` (`LEG`). The two vocabularies have **zero** overlap across
all 1730 concepts.

The inherited scripts joined them directly and read the result with
`dict.get(pair, {})` followed by `.get("family_count", 0)`. Two layers of default
turned a total join failure into a column of zeros, and a column of zeros sorted
into what looked like a ranked table but was alphabetical order over a constant.

The fix is to normalise names into slug space (`slugify`) and work there
throughout, converting back only for display. Verified bijective: all 1725
concept names in `colexifications.csv` map to distinct slugs, all present in
`forms.csv`. The five extra slugs in `forms.csv` — `january`, `june`, `nextyear`,
`pelican`, `poet` — are concepts that never colexify with anything, so they
legitimately have no row in the aggregated table.

The general lesson is about the defaults, not the case convention. A join whose
misses are indistinguishable from real zeros cannot be checked by looking at the
output. `src/test_clics.py` now asserts eight published family counts, so a
recurrence fails loudly.

## Defect 2: the Form column means different things in different varieties

CLICS4 pools wordlists that disagree about what `Form` holds. Across the five
English varieties:

| Variety | `Form` for SEA | Convention |
|---------|----------------|------------|
| 29 | `sea` | orthographic |
| 291 | `siː` | bare IPA |
| 632 | `siː` | bare IPA |
| 2625 | `s.iː` | dot-separated IPA |
| 2760 | `s.i` | dot-separated IPA |

The predecessor's plan for a homophone filter — flag pairs whose `Segments` match
but whose `Form` differs — assumes `Form` is a spelling. Run over a phonetic
variety it compares IPA to IPA, finds a match by construction, and pronounces
every homophone genuine. Implemented naively, the filter reported `sea`/`see`,
`son`/`sun`, `meat`/`meet` and `weak`/`week` as real colexifications, because a
phonetic variety supplied an identical `Form` for both members of each pair.

The fix has two parts. `is_phonetic_form` recognises a transcription by
normalising away dots, spaces and stress marks and comparing to the `Segments`
string; phonetic varieties are then excluded from the spelling comparison.
`orthographic_key` strips parenthesised material, because English variety 29
records FOREST as `wood(s)` and WOOD as `wood` — one word with an editorial note
about number, which the raw comparison had been reporting as two spellings and
hence as a homophone.

The flag is deliberately tri-state. `True` means spelled differently in every
variety that recorded spellings; `False` means a shared spelling somewhere;
`None` means no variety recorded spellings at all, which is the normal case for
Russian and Japanese. Collapsing `None` into `True` would discard most non-English
data on the strength of evidence that was never collected.

### The filter matters less than expected

Once family counts were correct, no pair above the five-family threshold was
flagged as a homophone in any language pair tested. Every classic English
homophone sits at one to three families and is already excluded by the count.

The interpretation is that the two signals are largely redundant, and the
cross-linguistic one is stronger. Accidental homophony is by definition confined
to the language where the sounds happened to collide, so it cannot accumulate
family counts. This also inverts the handoff's framing: it lists the homophone
filter as unfinished business, but it is the *broken family counts* that made the
inherited tables unusable, and repairing those removes most of the noise the
filter was meant to catch.

The filter still earns its place for pairs near the threshold, and as an
independent check that does not rely on the aggregated graph being right.

## Defect 3: manufactured colexifications from multi-alternative cells

Spanish variety 12 answers the concepts HE, SHE and IT with one source cell,
`él/ ella/ ello`. CLICS4 splits that cell into three forms and attaches all three
to all three concepts. The nine resulting rows include a full cross-product, so
the extraction sees HE and SHE sharing a pronunciation and records a
colexification. Spanish `él` and `ella` are distinct words; the colexification is
an artifact of the split.

This is not rare. Among the varieties for English, Spanish, Russian and Japanese,
1348 of 8817 concept-in-variety entries carry more than one distinct
pronunciation, and inspection shows many are alternative-listing cells:
`hermano/ hermana` for SIBLING, `primo/ prima` for COUSIN, `nosotros/ nosotras`
for both inclusive and exclusive WE.

The `alternatives_only` flag fires when every variety supporting a pair has *both*
concepts holding two or more distinct pronunciations. A genuine colexification is
normally recorded as a single shared word — Spanish `carne` appears once under
FLESH and once under MEAT — so requiring at least one single-word attestation
separates the two cases. It clears the Spanish pronoun rows while leaving
FLESH/MEAT, WOMAN/WIFE, LEG/FOOT and HEAR/LISTEN untouched.

It is a heuristic and is reported rather than applied destructively. A language
can genuinely have synonyms for both halves of a real colexification, and such a
pair would be flagged wrongly.

### The part that cannot be fixed here

Japanese variety 1316 records the single form `kaɾe` under HE, SHE and IT alike.
That is an error in the source wordlist — Japanese has `kare`, `kanojo` and
`sore` — but structurally it is identical to a genuine colexification: one
concept, one word, repeated. No filter operating on the CLICS4 tables can
separate them, and the Japanese pronoun rows accordingly survive every check and
sit at the top of the Japanese asymmetry table on a family count of 226.

`test_clics.py` asserts this gap explicitly, so it stays visible.

## A distinction the tables invite readers to miss

Ranking is by global family count, which measures how often the pair is
colexified *anywhere*. Whether the pair is reliably attested *in the language of
interest* is a separate question, evidenced by `n_varieties_here`.

The Japanese pronoun rows are exactly this trap. Their family count of 226 is
real: gender-neutral third-person pronouns are common across the world's
languages. The Japanese attestation behind it is not. A high family count says
the concept pair is a plausible place for languages to merge; it says nothing
about whether this language does.

## What the rebuilt tables show

Filters applied: family count at least 5, not flagged as homophone, not flagged
as an alternatives-only expansion.

| Direction | Raw pairs | Surviving |
|-----------|-----------|-----------|
| Spanish colexifies, English distinguishes | 127 | 79 |
| English colexifies, Spanish distinguishes | 91 | 25 |
| Russian colexifies, English distinguishes | 14 | 13 |
| English colexifies, Russian distinguishes | 106 | 40 |
| Japanese colexifies, English distinguishes | 265 | 80 |
| English colexifies, Japanese distinguishes | 96 | 30 |

The three pairs the predecessor built the test set around all reappear at the top
of their respective tables — Russian FOOT/LEG at 100 families, Spanish WIFE/WOMAN
at 59, Japanese HEAR/LISTEN at 53 — so the fixes vindicate the original selection
rather than overturning it.

Candidates the inherited analysis did not surface, all of which have the same
underspecification character as LEG/FOOT:

- **Russian FINGER/TOE**, 39 families, `палец`. The closest structural analogue
  to LEG/FOOT in the same language, and equally underspecified in isolation.
- **Russian LANGUAGE/TONGUE**, 13 families, `язык`. Widely known, and English
  itself colexified these until recently.
- **Russian HOME/HOUSE**, 16 families, `дом`. English forces a choice that is
  affective rather than physical.
- **Japanese LOWER ARM/UPPER ARM**, 199 families, `腕 ude`. The highest-count
  body-part asymmetry found, and English has no single word covering both.
- **Japanese TREE/WOOD**, 58 families, `木 ki`. Listed in the handoff as a
  possibility; confirmed here.
- **Japanese CLAW/FINGERNAIL**, 65 families, `爪 tsume`.
- **Japanese LANGUAGE/WORD**, 47 families, `言葉 kotoba`.
- **Spanish DISH/PLATE**, 43 families, `plato`, and **FOOD/MEAL**, 40 families,
  `comida`.

Russian's table is short — 14 pairs before filtering — because CLICS4 holds only
two Russian varieties with limited concept coverage. Short is not the same as
sparse: 13 of the 14 survive filtering, the highest pass rate of any direction
tested, so what little is there is comparatively clean.

## Reproducing

```bash
src/setup_clics4.sh
python3 src/test_clics.py
python3 src/extract_asymmetries.py russian english
```
