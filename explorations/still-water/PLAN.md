# Still Water: plan

Goal (asked by the user, 2026-10-21): a browser game that makes backpropagation intuitive. The user
rejected an adversarial "blame" framing and asked for a peaceful, zen "seek the natural balance"
metaphor.

## Metaphor (each garden word is one network word)

| Garden | Network |
|---|---|
| spring | input x |
| channel and its gate stone | weight w (teal channel: positive, plum: negative, draws water away) |
| middle pool, its water level | hidden unit, its activation |
| basin, its water level | output, the prediction y-hat |
| natural level | target y |
| ripple height (the meter) | loss L = 1/2 sum (y-hat - y)^2 |
| Listen: ripples travel upstream | backward pass |
| arrow and ring at a gate | dL/dw: which way the gate should move, and how strongly |
| a breath | one gradient-descent step, all weights at once |
| breath depth | learning rate eta |
| stillness | loss below 5e-4 |

## Levels ("gardens"), one idea each

1. The first stream: one input, one weight; drag by hand. Training = turn knobs until output matches.
2. Listening: two inputs; ripples show direction; the larger input's gate ripples more (dL/dw = err * x).
3. One breath: no hand dragging; breathe; every gate moves at once (gradient step).
4. Breath depth: learning rate; too small crawls, too large overshoots/diverges; best = 1/sum x^2.
5. A pool between: chain rule through a sigmoid (err * w2 * h(1-h) * x).
6. Where streams part: one hidden pool, two outputs; ripples add, here cancel (sum over paths).
7. The dry pool: ReLU unit with negative input passes no gradient (dead unit); can be revived by hand.
8. The brimming pool: saturated sigmoid; tiny slope, learning stalls; drag it to the middle first.
9. The whole garden: the class 2 regression example (x = (2,1), y = 2), with biases; numbers match the slides.

## Decisions
- One self-contained HTML file (`still_water.html`), no libraries; also published as a private artifact.
- Exact math (no fudging): forward/backward in plain JS, checked against finite differences in `tests/check.js`.
- Calm: no timer, no failure; stones (1-3) for breaths within par. Progress kept in localStorage if available.
- "Show the numbers" toggle maps every picture to its quantity, so it doubles as a study aid.

## Status
- [x] build `still_water.html`
- [x] tests: gradients vs finite differences, play every garden to stillness, check pars, no console errors (garden 8 par raised 6 -> 8: the hint asks for a few stuck breaths first)
- [x] publish (private artifact: https://claude.ai/artifact/EskWqGAYCn6Gh7Aj6j2CaL), commit
