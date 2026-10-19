# Notes

## Design decisions

- Size: 48 × 36 in landscape (4608 × 3456 CSS px at 96 px/in). Not specified by the user; chosen as a common US conference size. Changing it means re-flowing the three columns.
- Layout: left column = title, (1) the G-V gap, (2) theory, (3) FLORA; center = main finding, Figure 5, QR codes; right column = (4) results, ablation, validator, limits.
- Type: Archivo (display and body), STIX Two Text (math). Colors: ink #14161A, generator blue #2F5D9B, FLORA orange #D2601A, baseline grey #7D838C. Blue/orange pair passes the dataviz palette validator (CVD ΔE 21.7).
- The noble-gas diagram is a redrawn illustration of the paper's Figure 1, not data. Bar heights are invented and labeled as an illustration.
- Figure 5 is the paper's raster PNG (2027 px wide), printed about 19.5 in wide, so roughly 100 dpi. A vector or higher-resolution export from the paper source would print sharper.

## How the headline numbers were derived (all from Table 2)

"Strongest alternative" = best of untrained model, SFT, Consistency FT, RankAlign, per setting and metric. FLORA = better of FLORA-PMI and FLORA-Neg, per setting and metric. This matches how the paper's text computes "+27 pp" and "+7.3 pp".

- ρ +0.27: IFEval/Gemma-2-9b-it, 62.8 vs 35.5 (untrained); also HumanEval/Gemma-4-31b-it, 76.3 vs 49.0 (Consistency FT).
- AUROC +7.3: HumanEval/Gemma-4-31b-it, 94.2 vs 86.9 (RankAlign).
- Excluding the untrained model, the largest gains are larger: ρ +0.33 and AUROC +10.2 (both IFEval/Gemma-2-9b-it).
- FLORA AUROC: best in 4 settings, tied in 1 (Hyponymy/Qwen, 88.2), behind in 1 (HumanEval/Qwen: 88.9 vs SFT 94.1).
- FLORA ρ: best in 3 settings; behind RankAlign by 1.0 (HumanEval/Qwen), 1.4 (Hyponymy/Gemma), 1.0 (Hyponymy/Qwen).
- Validator (Table 5): Acc_V change ranges per setting are in `make_charts.py` output. Largest ROC_V drop is 0.4 (Hyponymy/Gemma-2-9b-it, 94.9 → 94.5).

## Inconsistencies found in the paper (arXiv v1)

These affect what the poster can safely claim. Worth fixing in the paper.

1. Section 6.1 says both corrections improve ROC_G and ρ "on all tasks", but Table 1 shows HumanEval ρ falling with s_PMI (34.1 raw → 22.4).
2. Table 1's IFEval rows (Gemma-2-9b-it: raw 57.5, PMI 81.0, Neg 64.5) do not match Table 2's IFEval Base row (78.2 / 35.5). HumanEval and Hyponymy Base rows do match a Table 1 row. Cause unknown.
3. Table 3's caption says Gemma-2-9b-it, but its HumanEval row (94.2 / 76.3) equals Table 2's FLORA-Neg on Gemma-4-31b-it, and Gemma-2-9b-it was excluded from HumanEval (Section 5.2). The poster labels that row Gemma-4-31b-it. This is an inference.
4. Section 6.2 text says the largest Table 3 drop is on HumanEval (−6.3 ROC_G), but IFEval drops more on ROC_G (85.1 → 78.5, −6.6). HumanEval has the largest ρ drop (−16.1).
5. Figure 4's caption says "all five settings" and "preserves or improves"; Table 5 has six settings, and Acc_V falls on both Hyponymy settings (by 0.6 to 2.5 points).
6. "Five out of six settings (tying RankAlign...)" for ROC_G counts the tie as a win; FLORA is behind on HumanEval/Qwen.
7. Small typos: "NegTC" (Sec. 6.1, should be NegFC), "w/o typ. corr." (Table 3), "v_a = 1" (Sec. 3.1, should be v_y), Eq. 8 cited as §3.1 (it is in §3.2).

## Not verified

- The QR code target https://github.com/juand-r/flora is copied from the paper's footnote; I did not check that the repository is public.

## Check against the final version of the paper (18-page PDF, received 2026-10-18)

Every number on the poster was checked against the final PDF.

- Tables 1, 2, 3 and 5 are identical to arXiv v1. `make_charts.py`'s `TABLE2` and `ACC_V` match the final PDF value for value (checked by script). The Figure 4 labels also match.
- All derived claims (+0.27 ρ, +7.3 AUROC, 5 of 6, 3 of 6, within 1.4, 0.4 validator AUROC drop) rest only on Tables 2 and 5, so they are unchanged.
- Figure 5 shows the same data and the same panel titles. Only the prompt header is restyled (italic quote instead of a boxed sentence). The final PDF embeds it at the same resolution (2027 px wide), so it has no sharper copy.
- Title, authors and affiliations are unchanged.

What the final version changes that matters for the poster:

- Appendix D (new, Table 7) evaluates open-ended generation, both sampled and greedy. FLORA leaves it roughly unchanged: HumanEval greedy 97.6 → 95.1, IFEval sampling 72.0 → 69.0 (p = 0.42), others equal or within 1 point. The poster's "Limits" box says "we do not test greedy outputs", which is now wrong. The final Limitations section says instead that FLORA does not demonstrate an improvement on greedy 1-best answers.
- Also new: Table 8 (MMLU 72.3 → 72.1, GSM8K 82.6 → 82.0, TruthfulQA 60.2 → 64.0), Table 9 (NLL-term ablation), a stability remark (RankAlign generator ROC std 6.0 vs ±1.4 for FLORA-PMI on IFEval/Qwen), and a selection rule for PMI vs Neg in Limitations.

New inconsistency in the final version: Table 9's "FLORA (full)" row for IFEval/Gemma-2-9b-it (ROC_G 85.1, ρ 61.7, ROC_V 79.6, Acc_V 66.2) differs from Table 2 (ρ 62.8) and Table 5 (ROC_V 79.4, Acc_V 63.6) for what appears to be the same model.

Of the v1 issues listed above, all of 1 to 7 are still present in the final version (checked: Sec. 6.1 "on all tasks", Table 1 vs Table 2 IFEval Base, Table 3 caption, "largest drops on HumanEval", Figure 4 "five settings", "five out of six", typos NegTC, "w/o typ. corr.", v_a, §3.1).

## A0 portrait version (2026-10-19)

- EMNLP 2026's poster printing page (https://2026.emnlp.org/poster-printing/) requires PDF, portrait, A0 (841 × 1189 mm). Board dimensions are not published there; no separate presenter page was found.
- Artboard 3179 × 4494 px (A0 at 96 px/in). Layout: header (title, authors, QR codes) → full-width band (main idea at 172 px, Figure 5 at 1780 px wide, subtext and figure notes beside it) → three 955 px columns (1 gap and 2 theory | 3 FLORA, ablation, validator | 4 results, limits).
- Content is the same as the landscape version except the Limits text, which follows the final paper (Table 7 tests sampled and greedy outputs): "Gains are in ranking fixed candidate sets; sampled and greedy outputs stay roughly unchanged."
- Checked by rendering: no overflow (root scroll height = 4494), column bottoms at 3902 / 4185 / 3988 px against a 4398 px limit. The Keynote kit reassembles into the poster at the listed positions.

## Editable A0 .pptx (2026-10-19)

- `build_pptx.js` renders `poster-a0.html` in Chromium with Keynote-safe type (font-stretch 100%; weights collapsed to 400 or 700, because Keynote reliably offers Archivo Regular and Bold), reads each element's box, paragraphs and runs (size, weight, italic, colour, sub/superscript, letter spacing), and writes them with pptxgenjs 3.12.0.
- With those fonts the layout still fits (the title wraps to two lines; everything below shifts down about 65 px; lowest column ends at 4251 px of 4494).
- Text boxes: 27; table: 1 (ablation); images: 9 (noble-gas diagram, equation, FLORA diagram, Figure 5 card, legend, two charts, two QR codes), captured at 2× from the same render.
- Checks: skill validator passes; LibreOffice render (with Archivo and STIX Two Text installed locally) shows no overflow and matches the poster. Superscripts were first shrunk twice (poster size × PowerPoint superscript); fixed by giving those runs the surrounding text size.
- The arrow "→" and Greek "ρ" are not in Archivo; LibreOffice and Keynote fall back to a system font for those glyphs, as the browser does.
