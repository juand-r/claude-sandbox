# queue (round 4): a queue machine with finite control in Rule 110

Avenue (e). Goal: extend Cook's verified glider queue so that what a read
appends depends on a carried state (not a cyclic tag system). Running log
with every result, scope and mistake: NOTES.md. Board posts: ../BOARD.md.

Everything is exact Rule 110. Scripts import round2/queue/splice.py and the
main project read-only (q.py). Python env: the main project's (numba).

Core tools
- lscene.py: exact local scenes cut from the full Cook machine (Ebar-frame
  window + light-cone margins); control in t_scene_ctl.py.
- reads.py: decoder-free multi-read check with mid-run surgery (VMULT env
  = ossifier spacing multiplier; use VMULT=2, see NOTES "baseline").
- zscreen.py / zlib.py / zmix.py: modifiers Z in front of the reader
  (rejector path); accZ_common.py / zaccpair.py: acceptor path.
- vequiv.py, rclass.py, dclass.py: V-class (debris) tests.
- create.py / create2.py: creation searches (table material before K).
- zconv.py / zconv2.py: answer converters right of the reader.
- pstar.py: modified readers, both paths (class-as-state).

Status: first milestone (a machine-created state-dependent read) NOT
reached. Verified: forced-N reader modifiers (surgery), the debris
V-class law, the extra-crossing mod-8 law, path symmetry of readers.

Key reproduce commands
- Forced-N read, full machine, then 6 correct reads (tape NYYN):
  `VMULT=2 python t_zfull.py NYYN 8 "Ebar:15:-36;E^3:3:-12" KF`
  (negative control: same with NNYY fails at read 2).
- Exact consumed modifier control: `VMULT=2 python t_zfull.py NYYN 8 "Ebar_8_Ebar:5:-28" KK`.
- Crossing law: `python t_chain.py NYYN "0,-1053;0,-990"` (2 Ebars:
  garbage) vs `python t_chain.py NYYN "0,-1053;0,-990;0,-927;0,-864;0,-801;0,-738;0,-675;0,-612"`
  (8 Ebars: normal read, answer 7 periods early).
- Phase is not state: `python t_prep2.py 33000`.
- Debris classes: `python t_rc1.py "Ebar:15:-36;E^3:3:-12"` and
  `python rclass_batch.py` (remnant classes of forced-N families).
- Path symmetry of readers: `python pstar.py 22 125 2 out.jsonl` then
  `python ana_pstar.py out.jsonl` (5,252 cores; original = control).
- Creation searches: `VMULT=2 python create2.py 112 -10 102 out.jsonl`;
  `SPLITREL=25 VMULT=2 python selrep.py out.jsonl`.

Large regenerable tables (not committed): zmix*.jsonl (zmix.py runs listed
in zmix_queue*.sh), zpairs_rej.jsonl (zscreen.py -200 0 150).
