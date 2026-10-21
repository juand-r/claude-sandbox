# Notes: Tokens of Meaning poster

## Plan

- [x] Read the paper (17 pages, Sept 15 2026 build) and the user's final FLORA layout (v7).
- [x] Decisions from the user: A0 portrait; editable .pptx plus separate figures; one QR code to the GitHub repo.
- [x] Figures: cartoon band, evidence-pooling sketch, decision procedure, spelling normalization, results chart.
- [x] Poster page (HTML, A0 at 96 px/in = 3179 × 4494 px), checked for overflow (`check_layout.js`).
- [x] Editable .pptx for Keynote: 6 shapes, 36 text boxes, 3 number circles, 6 images. LibreOffice render matches the HTML; page size A0.
- [x] Render checks; send preview, .pptx and figure files.

## Layout (follows FLORA v7)

v7 geometry in points on the 2383 × 3370 pt slide:

| Part | v7 position | Fill |
| --- | --- | --- |
| Header (title, authors, QR) | y 0 to 272 | DAFEC2 at 37% on F6F7F5 = #ECFAE2 |
| Big tagline | y 293 to ~774 | none; key words in red BD0700 |
| Cartoon band | y 774 to 1510 | D2E2C8 |
| Left box (overview) | x 17, y 1538, 766 × 1758 | B0EBFF at 38% = #DBF2F9 |
| Method box | x 799, y 1541, 1562 × 1044 | CBD9FF at 32% = #E8EDF8 |
| Results box | x 795, y 2611, 1562 × 685 | C85DFF at 8% = #F2EAF6 |

Type in v7: headings 44 pt, body 25 pt, Archivo Regular/Bold. The vines, peppers and plant were the user's own images for FLORA; they are not reused.

The user asked to emphasize the idea and method, with only the best results, at the bottom.

## Facts used on the poster (all from the paper)

| Claim | Source |
| --- | --- |
| BabyLM strict-small budget: 10M words | Sec. 1, 4.2 |
| Children learn from tens of millions of words | Sec. 1 |
| wug test; walked/walking reinforce walk | Sec. 1 |
| Splits accepted only if (P) productive and (S) semantically related; S1 to S4 | Sec. 3.1, Fig. 1 |
| Keep-atomic examples: business (S1), adder (S2), limestone (S3), werewolf, singleton (S4), cranberry (P) | Table 1, Sec. 3.1 |
| nutrit recurs across nutrition/nutritious/nutritive | Sec. 3.1 (P3) |
| Lemma-level morphemes: -s/-es/-ies → -s; in-/im-/il-/ir- → in-; -ise/-ize | Sec. 3.3 |
| Built on MorphyNet; inflection table used directly (~988 repairs); derivation table only as candidates | Sec. 4.3 |
| 22,137 high-frequency words hand-segmented; ~53% of the MorphyNet derivational proposals they overlapped rejected | Sec. 4.3 |
| LLM agents (Claude Code) review candidates adversarially; author makes every final decision | Sec. 4.3 |
| 28,571 explicit decisions; ~10,000 change MorphyNet (1,114 splits rejected, 3,933 re-segmented, 4,961 added) | Sec. 4.3 |
| 36,638 morphemes; no subword fallback; OOV 0.99% of tokens; fertility 1.177 | Sec. 4.4, Table 4 |
| 41.9% of morphemes shared by two or more word forms; typical shared stem in ~3 forms, ~36% more exposure than its most frequent form | Sec. 5.1 |
| Segmentations in the cartoon (BPE, MorphPiece raw, Ours) | Table 2 |
| Controlled comparison: Ours 66.35 vs MorphPiece (raw) 64.96 BLiMP (+1.4); same model, data, seed | Table 3, Sec. 5.2 |
| COMPS: the three morphology-based tokenizers are the top three (57.10, 56.91, 56.74) | Table 3 |
| Submitted recipe (Muon + MNTP), only the tokenizer varies: Ours pruned 72.53, Unigram 67.97, Ours un-pruned 67.71, BPE 67.11, Morfessor 66.63, MorphPiece 65.89 BLiMP | Table 6 |
| Leaderboard (strict-small): 2nd on COMPS (54.67), 3rd on EWoK (53.2), BLiMP 72.53 | Sec. 1, 5.3, abstract |

Results deliberately left off the poster (the user asked for the best results only), but worth knowing when presenting:
- Plain autoregressive training: BPE beats Ours on BLiMP (67.26 vs 66.35). With MNTP the order reverses (67.71 vs 67.11). Table 3, Sec. 5.2.
- Ours loses determiner–noun agreement (−27) and superlative quantifiers (−39) on BLiMP. Sec. 5.2.
- Gains do not carry to (Super)GLUE. Limitations.
- The submitted tokenizer differs from the un-pruned one in two ways (pruning of rare morphemes and character backoff), so the 72.53 vs 67.71 gap is not curation alone.

## Open issues

- The QR code decodes to https://github.com/juand-r/morpheus-tokenizer, but `git ls-remote` without credentials asks for a login, so the repo is private or not yet created (checked 2026-10-20).
- Chip colours in the cartoon (meaningful / misleading / kept whole) are our reading of the paper's argument, not labels from the paper.

## Revision 2 (2026-10-21)

- Results: the big "2nd / 3rd" and "+1.4" numbers are now body-size sentences. Reason: none of the 32 BabyLM 2025 posters (babylm.github.io/posters_2025.html) shows rankings in large type; the one that mentions the leaderboard does it in a bullet, and the tokenization posters use compact tables.
- Title: middle dots mark morpheme boundaries, taken from the real tokenizer (HF repo juand-r/morpheus-10M-v5, `our_tokenizer.py`, run on each title word): token·s, mean·ing, semantic·ly (shown as Semantic·ally), inform·ed, morphology·ical (shown as Morpholog·ical), model·ing; tokenization, language, low, resource kept whole; low-resource split at the hyphen.
- Method box 60 px taller, Results box 60 px shorter, to balance empty space.
- Results chart: gridlines replaced by axis ticks. LibreOffice drew faint outlines wherever semi-transparent PNG pixels overlapped (label halos, gridlines); removing the overlap avoids depending on how Keynote composites them.
- Title dots: U+2219 (bullet operator) from Archivo, black, bold, 120% (user chose it from a rendered comparison of the three dots Archivo has: · square, • large round, ∙ small round).
- Google Fonts' Archivo "latin" subset lacks U+2219, so the preview fell back to another font's square dot. The poster now loads the full Archivo 2.001 TTFs from `assets/fonts/` (SIL OFL); the Google Fonts download zip has the same glyph, so Keynote shows the round dot.
- Title reverted to plain text at the user's request. The ∙ dots moved to the banner, again from the real tokenizer: word·s, morpheme·s, piece·s, mean·ing; split, into, only, when, the, keep stay whole. Dots take the colour of their word (red inside the red words).
