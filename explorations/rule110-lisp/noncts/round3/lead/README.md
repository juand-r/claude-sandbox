# Lead's spot-checks of round-3 claims

Re-run by the lead with the agents' own scripts:
- `lead3_t2.log`: `verify/t2_demo_check.py 9`, the T2 integration (both
  coupling directions in one run): v1 = 0..9, 0 mismatches, left-program
  placements identical across inputs, three controls fail. This is the
  cross-check verify's report asked for (same scripts, separate run).
- `lead3_left.log`: `leftstream/rand_test.py 30 16 8 7`, 30 random
  left-stream programs of length 16 over {INC, DEC, zero test}, inputs
  0..8, with a seed (7) the agent never used: 270/270 runs = model.
