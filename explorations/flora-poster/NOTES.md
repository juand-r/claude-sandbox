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
