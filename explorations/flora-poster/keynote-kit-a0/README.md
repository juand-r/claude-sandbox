# Keynote kit

Every element of the A0 portrait, 841 × 1189 mm poster as its own file, plus where it goes. See `layout-map.png` for the numbered map.

## Setting up the slide

1. In Keynote, open the Document inspector and choose Slide Size > Custom: 2384 × 3371 pt (A0 portrait, 841 × 1189 mm at 72 pt per inch).
2. Draw the background rectangles (S1, S2) from the table and send them to the back.
3. Drag in each file from `pdf/` and type its x, y, width and height into the Arrange inspector. Positions are the top-left corner.

Use the PDFs: they are vector, so text and charts stay sharp at any size, and the fonts are embedded. The `png/` folder has the same elements as transparent PNGs (192 px per printed inch) in case you prefer images. Text inside these files is not editable; `copy.md` has all the text if you want to retype a block as a Keynote text box (fonts: Archivo and STIX Two Text, both free on Google Fonts).

## Positions (points, slide 2384 × 3371 pt)

| id | element | x | y | w | h | fill |
|---|---|--:|--:|--:|--:|---|
| S1 | background | 0 | 0 | 2384 | 3371 | #F6F7F5 |
| S2 | center-band | 0 | 367 | 2384 | 1134 | #E6ECF4 |
| 01 | title-block | 72 | 96 | 1716 | 223 |  |
| 02 | qr-paper | 1860 | 72 | 211 | 247 |  |
| 03 | qr-code | 2113 | 72 | 200 | 247 |  |
| 04 | main-idea | 72 | 439 | 2240 | 399 |  |
| 05 | figure-scatter | 72 | 886 | 1335 | 544 |  |
| 06 | main-subtext | 1461 | 886 | 851 | 224 |  |
| 07 | figure-notes | 1461 | 1140 | 851 | 183 |  |
| 08 | s1-heading | 72 | 1549 | 716 | 95 |  |
| 09 | s1-text | 72 | 1660 | 716 | 145 |  |
| 10 | s1-noble-gas-diagram | 72 | 1827 | 716 | 594 |  |
| 11 | s2-heading | 72 | 2461 | 716 | 47 |  |
| 12 | s2-text | 72 | 2524 | 716 | 110 |  |
| 13 | s2-equation | 72 | 2651 | 716 | 202 |  |
| 14 | s2-note | 72 | 2870 | 716 | 57 |  |
| 15 | s3-heading | 834 | 1549 | 716 | 47 |  |
| 16 | s3-text | 834 | 1613 | 716 | 72 |  |
| 17 | s3-flora-diagram | 834 | 1702 | 716 | 360 |  |
| 18 | s3-note | 834 | 2078 | 716 | 87 |  |
| 19 | ablation-title | 834 | 2204 | 716 | 33 |  |
| 20 | ablation-note | 834 | 2250 | 716 | 55 |  |
| 21 | ablation-table | 834 | 2318 | 716 | 197 |  |
| 22 | ablation-footnote | 834 | 2529 | 716 | 27 |  |
| 23 | validator-title | 834 | 2595 | 716 | 33 |  |
| 24 | validator-note | 834 | 2642 | 716 | 55 |  |
| 25 | validator-chart | 834 | 2710 | 716 | 320 |  |
| 26 | validator-takeaway | 834 | 3043 | 716 | 96 |  |
| 27 | s4-heading | 1596 | 1549 | 716 | 47 |  |
| 28 | s4-definitions | 1596 | 1610 | 716 | 142 |  |
| 29 | results-title | 1596 | 1776 | 716 | 33 |  |
| 30 | results-legend | 1596 | 1822 | 716 | 29 |  |
| 31 | results-chart | 1596 | 1864 | 716 | 725 |  |
| 32 | results-takeaway | 1596 | 2602 | 716 | 128 |  |
| 33 | results-footnote | 1596 | 2744 | 716 | 79 |  |
| 34 | limits-title | 1596 | 2862 | 716 | 33 |  |
| 35 | limits-text | 1596 | 2905 | 716 | 86 |  |

The same table is in `elements.csv`. Regenerate everything with `node export_kit.js a0` from the folder above.
