# Keynote kit

Every poster element as its own file, plus where it goes. See `layout-map.png` for the numbered map.

## Setting up the slide

1. In Keynote, open the Document inspector and choose Slide Size > Custom: 3456 × 2592 pt (48 × 36 in at 72 pt per inch).
2. Draw the two background rectangles (S1, S2) from the table and send them to the back.
3. Drag in each file from `pdf/` and type its x, y, width and height into the Arrange inspector. Positions are the top-left corner.

Use the PDFs: they are vector, so text and charts stay sharp at any size, and the fonts are embedded. The `png/` folder has the same elements as transparent PNGs (192 px per printed inch) in case you prefer images. Text inside these files is not editable; `copy.md` has all the text if you want to retype a block as a Keynote text box (fonts: Archivo and STIX Two Text, both free on Google Fonts).

## Positions (points, slide 3456 × 2592)

| id | element | x | y | w | h | fill |
|---|---|--:|--:|--:|--:|---|
| S1 | background | 0 | 0 | 3456 | 2592 | #F6F7F5 |
| S2 | center-panel | 930 | 0 | 1596 | 2592 | #E6ECF4 |
| 01 | title-block | 72 | 72 | 804 | 433 |  |
| 02 | s1-heading | 72 | 538 | 804 | 49 |  |
| 03 | s1-text | 72 | 605 | 804 | 153 |  |
| 04 | s1-noble-gas-diagram | 72 | 782 | 804 | 558 |  |
| 05 | s2-heading | 72 | 1373 | 804 | 49 |  |
| 06 | s2-text | 72 | 1440 | 804 | 117 |  |
| 07 | s2-equation | 72 | 1575 | 804 | 214 |  |
| 08 | s2-note | 72 | 1807 | 804 | 29 |  |
| 09 | s3-heading | 72 | 1870 | 804 | 49 |  |
| 10 | s3-text | 72 | 1937 | 804 | 77 |  |
| 11 | s3-flora-diagram | 72 | 2031 | 804 | 360 |  |
| 12 | s3-note | 72 | 2409 | 804 | 93 |  |
| 13 | main-idea | 1026 | 126 | 1404 | 742 |  |
| 14 | main-subtext | 1026 | 940 | 1365 | 218 |  |
| 15 | figure-caption | 1026 | 1263 | 1404 | 69 |  |
| 16 | figure-scatter | 1026 | 1350 | 1404 | 574 |  |
| 17 | figure-panel-labels | 1026 | 1942 | 1404 | 62 |  |
| 18 | qr-paper | 1026 | 2298 | 481 | 204 |  |
| 19 | qr-code | 1579 | 2298 | 468 | 204 |  |
| 20 | s4-heading | 2580 | 72 | 804 | 49 |  |
| 21 | s4-definitions | 2580 | 136 | 804 | 118 |  |
| 22 | results-title | 2580 | 295 | 804 | 35 |  |
| 23 | results-legend | 2580 | 344 | 804 | 30 |  |
| 24 | results-chart | 2580 | 387 | 804 | 617 |  |
| 25 | results-takeaway | 2580 | 1017 | 804 | 99 |  |
| 26 | results-footnote | 2580 | 1130 | 804 | 82 |  |
| 27 | ablation-title | 2580 | 1254 | 804 | 35 |  |
| 28 | ablation-note | 2580 | 1302 | 804 | 55 |  |
| 29 | ablation-table | 2580 | 1370 | 804 | 201 |  |
| 30 | ablation-footnote | 2580 | 1585 | 804 | 27 |  |
| 31 | validator-title | 2580 | 1654 | 804 | 35 |  |
| 32 | validator-note | 2580 | 1702 | 804 | 55 |  |
| 33 | validator-chart | 2580 | 1770 | 804 | 347 |  |
| 34 | validator-takeaway | 2580 | 2130 | 804 | 66 |  |
| 35 | limits-title | 2580 | 2238 | 804 | 35 |  |
| 36 | limits-text | 2580 | 2283 | 804 | 61 |  |

The same table is in `elements.csv`. Regenerate everything with `node export_kit.js` from the folder above.
