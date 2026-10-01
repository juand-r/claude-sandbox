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
