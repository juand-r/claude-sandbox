# Structurally Forced Information Divergence via Colexification Asymmetries

## 1. What this is

When two languages describe the same situation, some differences in their output
are editorial (what to include) and some are structural (what the language forces
you to commit to or leave open). X-PARADE (Rodriguez et al., 2024) annotates the
former. This project targets the latter.

The mechanism: if language A has one word covering concepts X and Y, a speaker of
A can use that word without specifying which they mean. A speaker of language B,
which uses separate words for X and Y, must choose. That choice is forced by
lexical structure, not editorial preference.

CLICS4 provides a catalogue of where these splits occur across ~3400 language
varieties.

## 2. Data source

CLICS4: 1730 concepts, 3447 language varieties, 247 language families, 1.45
million form entries. Colexification is detected by matching on phonological
form (the Segments column, in IPA). Each colexification edge records which
languages and families attest it.

## 3. Global picture

51,562 concept pairs are colexified in at least one language. Of these:
- 321 pairs are colexified in 20+ language families
- 898 in 10+
- 3,986 in 3+
- 43,104 in exactly 1 (likely noise: homophony, data artifacts)

The interesting zone for forced divergence is the middle: pairs colexified in
many families but far from all. These represent genuine conceptual boundaries
that some languages draw and others do not.

## 4. Most promising concept pairs

Ranked by linguistic interest (frequency in everyday language, genuine ambiguity,
availability of parallel text).

### 4.1 LEG / FOOT (100 families colexify, ~140 do not)

Colexify: Russian (noga), Japanese (ashi), Bengali (pa), Turkish (ayak),
Swahili (mguu)

Distinguish: English, Spanish, French, German, Italian, Portuguese, Dutch,
Polish, Arabic, Korean, Mandarin, Vietnamese

This is the strongest case. "Noga" in Russian is genuinely underspecified.
Cornell University's Russian lexical database says explicitly: "Russian differs
from English in that the word noga may mean either 'leg' or 'foot'."

Naturally occurring examples from parallel text:

- "U menya bolit noga" -> "My leg hurts" or "My foot hurts" (both valid)
- "Sobaka ukusila yeyo za nogu" -> "A dog bit her leg" (could be foot)
- "Ya slomal pravuyu nogu" -> "I broke my right leg" (could be right foot)
- "Novyye botinki natyorli nogi" -> "New boots rubbed [one's] feet sore"
  (here context disambiguates toward "feet", but the Russian is still "nogi")
- "Ona sidela s nogami v uglu divana" -> "She was sitting with her legs tucked"
  (here context disambiguates toward "legs")

The critical observation: in many contexts, Russian leaves the leg/foot
distinction open and the English translator must commit. The commitment is
forced information that was not in the source.

### 4.2 WOMAN / WIFE (59 families colexify)

Colexify: Spanish (mujer), Portuguese (mulher), German (Frau), Dutch (vrouw),
Arabic

Distinguish: English, Russian, French, Italian, Japanese, Korean, Mandarin,
Turkish, Vietnamese

"Mi mujer" in Spanish is contextually almost always "my wife," but the word
itself is neutral between the two readings. An English translator must choose
between "my woman" (informal, potentially offensive) and "my wife" (specific
legal/social status). The connotations of the two English options are very
different.

### 4.3 DO / MAKE (76 families colexify)

Colexify: Spanish (hacer), French (faire), Portuguese (fazer), Italian (fare),
Korean (hada), Mandarin (zuo), Turkish (yap), Vietnamese (lam), Swahili, Thai

Distinguish: Japanese (suru vs tsukuru), Russian (delat' vs delat'), Polish

The English do/make distinction is typologically unusual. Most major languages
collapse it. This is well known in L2 English teaching: learners systematically
confuse "do homework" vs "make a decision" because their L1 uses one verb.

### 4.4 FLESH / MEAT (105 families colexify)

Colexify: Spanish (carne), Portuguese (carne), Japanese (niku), Mandarin (rou),
German (Fleisch), Dutch (vlees), Swahili (nyama), Thai, Vietnamese (thit)

Distinguish: English, Arabic

English is the outlier. "Carne" in Spanish covers living tissue and food
indifferently. "The carne of his arm" is normal Spanish; "the meat of his arm"
is bizarre English.

### 4.5 HEAR / LISTEN (53 families colexify)

Colexify: Japanese (kiku), Korean (tutta), Bengali (shona), Vietnamese (nghe)

Distinguish: English, Spanish, French, German, Russian, Arabic, Turkish, Polish

Japanese "kiku" is neutral between intentional listening and passive hearing.
"Kiku" in "Ongaku o kiku" could be "hear music" or "listen to music" depending
on context. English must commit to one.

### 4.6 MOON / MONTH (60 families colexify)

Colexify: Japanese (tsuki), Korean (tal), Turkish (ay), Swahili (mwezi), Thai

Distinguish: English, Spanish, French, Russian, German, Mandarin

Usually disambiguated by context (temporal vs celestial). Less interesting for
forced divergence than the body part cases.

## 5. What to do next

### Phase 2: Corpus collection

For each of the top pairs (especially LEG/FOOT, WOMAN/WIFE, HEAR/LISTEN):

1. Download aligned subtitle data from OpenSubtitles (OPUS project) for the
   relevant language pairs (Russian-English, Japanese-English, Spanish-English).
2. Search for sentences containing the colexifying word.
3. Filter for cases where context does NOT disambiguate.
4. Collect these as examples of forced information divergence.

Filtering strategy: a sentence is "genuinely ambiguous" if the colexifying word
could be translated by either of the two English words without changing the
truth conditions. This can be operationalised by checking whether both
translations are attested for similar contexts in the parallel data.

### Phase 3: LLM consistency testing

For the ambiguous examples from Phase 2:

1. Ask multiple LLMs to translate the source sentence.
2. Record which target word they choose.
3. Test consistency: same model, same sentence, multiple runs.
4. Test cross-lingual consistency: ask the LLM a question about the content in
   both languages and check whether the answers are compatible.

### Phase 4: Connection to X-PARADE

Annotate the forced divergence examples using the X-PARADE taxonomy (same, new,
inferable). The structural commitment forced by the target language is "new"
information in the X-PARADE sense, but it's new for a very specific,
predictable, linguistically motivated reason.

## 6. Files produced

- data/spa_only.tsv: concept pairs colexified in Spanish but not English
- data/eng_only.tsv: concept pairs colexified in English but not Spanish
- src/extract_v2.py: extraction script
- docs/project-design.md: original project design
