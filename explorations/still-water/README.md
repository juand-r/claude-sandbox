# Still Water

A calm browser game that teaches backpropagation. A small neural network is drawn as a water garden:
springs (inputs) feed channels (weights) into pools (units). Bring the last pool to its natural level
(the target). "Listen" sends ripples upstream, which is the backward pass; each breath moves every gate
along its ripple, which is one gradient-descent step. Nine short gardens, one idea each (see PLAN.md).

Run: open `still_water.html` in any browser. No install, no network needed (fonts fall back if offline).

Test (from `tests/`): `NODE_PATH=$(npm root -g) node check.js` checks every gradient against finite
differences, plays each garden to stillness, and checks the par breath counts.
