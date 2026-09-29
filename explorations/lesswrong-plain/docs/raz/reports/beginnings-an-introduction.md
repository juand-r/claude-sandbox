# Report: beginnings-an-introduction

## 1. The argument in three sentences

Book VI, *Becoming Stronger*, is presented as a call to action, so the introduction points
the reader to further reading: the book's Bayesian definition of normative rationality is
standard in cognitive science, while its philosophical positions (one-boxing on Newcomb's
problem, an optimality criterion for priors as in Jaynes and Hutter, the charge that
frequentism is the more "subjective" view) are more controversial, and Drescher's *Good and
Real* covers much of the same ground. It separates the philosophical dispute between
Bayesians and frequentists from the practical choice of statistical methods, and cites
evidence that statistical training, unlike classes in logic, improves everyday reasoning.
It then previews the book's three sequences and their questions, credits the original posts
with inspiring *Less Wrong*, the effective altruism movement and CFAR, and closes by saying
that the art of rationality is young and much is left undone.

## 2. Sources checked

Fetched files are in `data/sources/6a_beginnings-an-introduction/` (shared by my three
slugs). `insert_notes.py` inserts notes from `notes_<post>.py` into the saved skeletons
`skel_<slug>.tex`.

- PhilPapers 2009 survey, all respondents: `data/sources/5c_newcomb/pp2009.txt` (fetched by
  the Newcomb agent from https://philpapers.org/surveys/results.pl). Matched: "Newcomb's
  problem: one box or two boxes? Other 441 / 931 (47.4%) Accept or lean toward: two boxes
  292 / 931 (31.4%) Accept or lean toward: one box 198 / 931 (21.3%)". These are all
  respondents, not decision theorists; the note says "respondents".
- PhilPapers 2020 survey, decision theorists: Bourget and Chalmers, "Philosophers on
  Philosophy: The 2020 PhilPapers Survey", Philosophers' Imprint 2023
  (`data/sources/5c_newcomb/pp2020_paper.txt`), Table 26. Matched: "Decision Theory
  Newcomb’s problem: one box 22.7 46.1 −23.4 *"; header "Column S is the percentage of
  non-“other” answers among specialists"; text "Newcomb’s problem (decision theorists favor
  two-boxing)". Note: the introduction cites the 2009 paper; the 2009 decision-theorist
  breakdown was not available to me, so the decision-theorist figure is from 2020 and the
  note says so.
- Talbott, SEP "Bayesian Epistemology", Fall 2013 archive,
  https://plato.stanford.edu/archives/fall2013/entries/epistemology-bayesian/
  (`sep_bayes_2013.txt`). Matched: "(b) Objective Bayesians (e.g., Jaynes and Rosenkrantz)
  emphasize the extent to which prior probabilities are rationally constrained."; "Jaynes
  identifies four general principles that constrain prior probabilities, group invariance,
  maximium entropy, marginalization, and coding theory".
- Yudkowsky, "Frequentist Statistics are Frequently Subjective" (LessWrong, 2009-12-04,
  id 9qCN6tRBtksSyXfHu; `lw_frequentist_subjective.txt`, via the GraphQL API). Matched:
  "My own response is that frequentist statistics are far more subjective than Bayesian
  likelihood ratios."; "Steven Goodman offers a nicely illustrated example"; the six-flip
  coin example with 11% and 3%.
- Kruschke 2010 (TiCS): abstract only, via NCBI eutils (`pubmed_kruschke.txt`). Full text
  is paywalled (cell.com 403; the indiana.edu link redirects to the university home page).
  A search-result summary said the paper states that p values depend on stopping
  intention; I did not quote Kruschke and the footnote note says only the abstract was
  available.
- Beautiful Probability notes (`annotated/posts/beautiful-probability.tex`): contain "A
  frequentist would answer that the stopping rule is part of the declared design" and the
  likelihood-principle discussion. My pointer relies on these.
- Wikipedia, "Gary Drescher" (`wp_drescher.txt`, action=raw): "he defends rigorously
  mechanistic materialism ... defending the Everett or Multiple Worlds Interpretation ...
  Drescher also provides treatments of the Prisoner's Dilemma and Newcomb's Problem".
  I did not confirm from the book itself that Drescher one-boxes; the note says only that
  the book treats these problems.
- Fong, Krantz and Nisbett 1986: full text not reachable (Deep Blue behind Cloudflare;
  dokumen.tips 403; OpenAlex has no abstract). WebSearch summary: taught "the formal
  properties of the law of large numbers" and found improved statistical reasoning on
  everyday problems. Schoemaker 1979: ScienceDirect 403; WebSearch summary: "examines whether
  statistically trained and untrained subjects differ in their strategies for risk
  assessment". Both summaries are from search results, not pages I read; the note says the
  claims about psychology and logic are unchecked.
- My Best and Worst Mistake, `data/originals/my-best-and-worst-mistake.md`: "One of my
  primary purposes in writing on *Overcoming Bias* is to leave a trail to where I ended up
  by accident" (asterisks dropped in the quotation).
- Manifest `data/manifests/rationality_az.json`: Book VI sections Yudkowsky's Coming of Age
  (298-310), Challenging the Difficult (311-316), The Craft and the Community (317-338).

## 3. Arithmetic

None beyond reading the survey percentages (21.3 < 31.4; 22.7 < 50).

## 4. Claims about other posts

- "Newcomb's Problem and Regret of Rationality" (order 296): its notes give the 2009 and 2020
  figures in full (report `newcomb-s-problem-and-regret-of-rationality.md` lines 32-34). I
  point there rather than repeat (STANDARDS 2.5).
- "Beautiful Probability" (188): frequentist answer and likelihood principle, as above.
- "My Best and Worst Mistake" (300): quoted above.

## 5. Not verified

- Kruschke 2010 beyond its abstract; Fong et al. 1986 and Schoemaker 1979 beyond search
  summaries. Reading Fong et al. (Cognitive Psychology 18:253) would settle whether it reports
  on psychology training or logic classes. The likely sources for those claims are Lehman,
  Lempert and Nisbett (1988, American Psychologist) for psychology and Cheng, Holyoak,
  Nisbett and Oliver (1986, Cognitive Psychology 18:293) for logic training, but I could not
  read their abstracts either (PubMed has no abstract for Cheng et al.), so I did not name
  them in a note.
- Whether Drescher one-boxes (believed, not checked).
- The textbooks in footnotes 1 and 2, and the claim that the Bayesian definition is
  "standard in cognitive science": described, not checked.
- Holt's Slate article: not fetched.

## 6. Judgment calls

- Preface convention applied: the influence claims (Less Wrong, effective altruism, CFAR)
  and the closing are described, not charged.
- The statistics-training note is an "unchecked" note, not a charge. The Response keeps it
  in one paragraph and the In short line mentions it; the editor may prefer to keep it out
  of the In short line, since it is a verification gap rather than a fault.
- Credit given: the introduction says the book's philosophy is "more controversial" and
  lists testing the book's prescriptions as future work.
- No reserved words used (the raz_check "Wrong" flags are "Less Wrong").
