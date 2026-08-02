# Structurally Forced Information Divergence via Colexification Asymmetries

## Motivation

When two languages describe the same situation, differences in their output can
arise from editorial choice (what to include) or from structural necessity (what
the language forces you to commit to or leave ambiguous). X-PARADE (Rodriguez
et al., 2024) annotates the former; this project targets the latter.

The mechanism: if language A colexifies concepts X and Y (one word covers both)
but language B distinguishes them (separate words), then:

- A speaker of A can use the shared word without committing to X or Y.
- A speaker of B covering the same content must choose.

That choice is forced by lexical structure, not by the speaker's intent. It is a
systematic, predictable source of cross-lingual information divergence.

CLICS4 provides a catalogue of colexification patterns across ~3400 language
varieties. We use it to identify, for a given language pair, exactly where these
forced divergences should arise, and then look for naturally occurring text where
they do.

## Research Questions

1. For a given language pair (starting with English-Spanish), which
   colexification asymmetries are most likely to produce forced divergences in
   naturally occurring text?

2. Can we find naturally occurring examples where the asymmetry creates genuine
   underspecification in one language that must be resolved in the other?

3. Do LLMs handle these cases consistently across languages? When translating or
   generating parallel content, do they resolve the underspecification in the
   same way humans do?

## Method

### Phase 1: Extract colexification asymmetries from CLICS4

For a chosen language pair (L1, L2):
- Identify all concept pairs colexified in L1 but not in L2 (and vice versa).
- Rank by: (a) frequency of the colexifying word in general usage, (b) semantic
  distance between the two concepts (larger distance = more interesting
  divergence), (c) number of other languages that also colexify the pair (if
  many do, it's likely underspecification rather than homophony).

Output: a ranked list of colexification asymmetries with metadata.

### Phase 2: Find naturally occurring examples

Sources to search (in order of promise):
- Subtitle corpora (OpenSubtitles): dialogue is less specific, more likely to
  use words in underspecified ways.
- Literary translations: translators must resolve ambiguities that the original
  author could leave open.
- Comparable news articles: same event, independently written.
- Wikipedia (least promising, as noted: factual text tends to disambiguate).

For each asymmetry from Phase 1, search for sentences in L1 where the
colexifying word is used in a context that does not disambiguate between the two
concepts. Then check whether the corresponding L2 text (if parallel) or
comparable L2 text commits to one reading.

### Phase 3: LLM consistency testing

For the naturally occurring examples found in Phase 2:
- Ask an LLM to translate the underspecified L1 sentence into L2. Does it pick
  X or Y? Is the choice consistent across runs? Is it the same choice a human
  translator made?
- Ask an LLM to answer a question about the content in both L1 and L2. Does the
  underspecification cause inconsistent responses?

## Language pair selection

Starting with English-Spanish because:
- X-PARADE covers this pair, enabling comparison.
- Both are high-resource, so corpus availability is good.
- They are from different branches of Indo-European, so colexification patterns
  should differ meaningfully.

Will extend to English-Chinese and English-Hindi (also in X-PARADE) if Phase 1
yields interesting asymmetries for those pairs.

## Deliverables

1. A ranked catalogue of colexification asymmetries for English-Spanish (and
   potentially other pairs), extracted from CLICS4.
2. A collection of naturally occurring examples where these asymmetries create
   forced information divergence.
3. An analysis of LLM consistency on these examples.
4. A write-up connecting these findings to the X-PARADE framework.
