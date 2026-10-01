# theory (round 4) - running log

Labels: [thm] proved for the model stated; [model] executable abstract model
with tests; [arg] argument; [hyp] hypothesis; [sim] exact Rule 110 run
(theory runs none unless stated).

## 2026-10-01 22:48 start
- Read: round4 README/BOARD, noncts/SUMMARY.md, round2/SUMMARY.md,
  round3/SUMMARY.md, round2/verify/THEORY.md, round3/theory/THEORY.md,
  scholar/THEORY.md, scholar/SURVEY.md, both verify ledgers,
  round2 address/gate READMEs.

## 23:06 mistakes
- Board post headed 23:12 written before running date -u (real 23:05). Posted a
  correction. Rule for myself: run `date -u` first, then write the header.
- 23:2x stopped census (PID 4038 python child; recorded PID 4037 was the wrapper - lesson: nohup nice ... & gives the wrapper PID only when nice is wrapped; check with ps)
- 23:1x MISTAKE: explore.pid was written to noncts/ (cwd of the caller, exactly the trap the kickoff warns about). Moved it into theory/. Always use absolute paths for pid files.
- 23:3x BUG found+fixed in ptm.py: (1) compounds expanded into collider 'parts' do not reassemble with build_row -> false 'dirty'; expand() is now identity; (2) added rephase(). Earlier pass_* results moved to trash/ (invalid). explore.jsonl also affected (library compounds with parts as heads) -> rerun.
- 23:4x ran passraw B (1 min) concurrently with passsearch B: briefly 2 heavy processes; avoid.
- 23:26 killed passsearch B (PID 8702, sh 8362): 3093 pairs, 3092 dirty; launched passraw A then D (sh PID in passraw.pid)
- 23:5x bouncer.py (route 14 model): first versions too slow (event sim of
  Goedel-sized counters with 400-step budgets; killed my own test processes
  by PID 11579/11577/11571 and 12207/12206). Fixed: integer geometry, only
  halting runs with registers <= 5 compared. Result: 197/197 exact,
  controls 59/197 and 59/197 fail.
