# Report: Searching for Bayes-Structure (order 192)

Agent batch 4a. Sources and scripts in `data/sources/4a_searching-for-bayes-structure/`.

## 1. The argument in three sentences (written before annotating)

Since true beliefs require mutual information with the world, and mutual information cannot be
created without breaking the second law, any mind that finds truth, and any useful part of one,
must have "at least a little" Bayesian structure. The author reports that each time a cognitive
process that does not look Bayesian is examined in full, the same complete Bayesian structure
turns up underneath, so that the search for it is one "quest" with one "Holy Grail". Knowing
only that a process is Bayesian is a password; the goal is "Bayes-Sight", seeing how.

## 2. Sources checked

- Wikipedia, "Ridge regression" (raw wikitext, fetched this session):
  `data/sources/4a_searching-for-bayes-structure/wiki_ridge.txt`, section "Bayesian
  interpretation". Matched: "Under these assumptions the Tikhonov-regularized solution is the
  [[maximum a posteriori|most probable]] solution given the data and the ''a priori''
  distribution of <math>x</math>, according to [[Bayes' theorem]]." (The post links the old
  "Tikhonov_regularization#Bayesian_interpretation" anchor; the article is now "Ridge
  regression".) Quoted in the note: "according to Bayes' theorem".
- Jaynes 1957 (Physical Review) as the source of "statistical mechanics as inference": not
  re-read here; the note is a pointer to the note on "The Second Law of Thermodynamics, and
  Engines of Cognition" (order 190), which makes the point in full with its sources.
- Epigraph (Spelljammer) and closing quotation (Zelazny, Prince of Chaos): not checked; the
  notes say so.

## 3. Arithmetic

- Inverted-map claim: if S is uniform on 2^10 states and the belief B is any bijection of S
  (for example one in which every belief is wrong), I(B;S) = H(S) = 10 bits. Checked in
  `data/sources/4a_searching-for-bayes-structure/check_probability.py` (last lines).
- "all Bayesian evidence is mutual information and all mutual information is Bayesian
  evidence": for two variables, I(X;Y) > 0 exactly when X and Y are dependent, i.e. when some
  value of one changes the probability of the other. Standard; no note depends on more.

## 4. Claims about other posts

- "Perpetual Motion Beliefs" is the previous day's post: posted 2008-02-27 per the manifest;
  this post 2008-02-28. Quoted words are this post's own ("the same sort of improbability").
- "The Second Law of Thermodynamics, and Engines of Cognition" (order 190): its first cpara
  says "The view that thermodynamic entropy measures an observer's information is E.~T.
  Jaynes's program (Physical Review, 1957), and it is contested". My clogic points there.
- "Conditional Independence, and Naive Bayes" (order 179), checked as the brief asked. Its
  clogic, Response and n.b. say this post "argues only that any part of a process that
  'contributes usefully to truth-finding must have at least a little Bayesian structure.' Its
  stronger claim, that the search always ends with 'the same Holy Grail,' is supported there
  by the author's account of repeated discoveries, not by that argument." That agent's
  judgment call asked whether "as it always must be" ties the strong claim to the argument.
  My reading after two readings of the post: the reading is fair. The argument's own
  conclusions are hedged ("at least vaguely Bayesian", "at least a little", "however
  noisily"); the "must" of the argument ("or it couldn't possibly work") is attached to that
  weak form; the strong claim is introduced with "always turns out" and supported by "Once
  this happens to you a few times". "As it always must be" in the last paragraph is ambiguous
  between the two; the argument backs it only in the weak sense. Also, the post itself calls
  knowing "that" a process is Bayesian "a hint ... certainly not an answer", which is what the
  argument gives. My notes make this point in full (Grail paragraph, Bayes-Sight paragraph,
  "Yes"/"No" list, password paragraph), so 179's short version is consistent with it. No
  change needed to 179.

## 5. Not verified

- Spelljammer epigraph wording and source (a 1989 boxed set; not reachable).
- Zelazny, Prince of Chaos (1991): passage not checked.
- The post's link on "Yes!" (YouTube) was not opened; no note depends on it.

## 6. Judgment calls

- The cpara on "In fact, any part ...": "So qualified, the claim comes close to restating its
  premise." A judgment about content, not a reserved word. The fair-defender reply would be
  that the thermodynamic argument adds physical necessity. I think the note survives because
  "Bayesian structure" is undefined in the post and the premise is "contributes usefully to
  truth-finding".
- The clogic on the inverted map: a technical clarification (mutual information is not
  accuracy). In context the previous paragraph assumes true beliefs, and the note says so, so
  it does not claim the argument fails. Could be cut as a nitpick if the editor prefers.
- The clogic on the "Yes"/"No" list: says the search, as described, has no outcome counting
  against the thesis. I avoided "unfalsifiable". The list is comic; test 3 (joke) was
  considered, and the note answers it by pointing to the next paragraph, which presents the
  monologue as how one learns "the rhythm".
- The philosophers paragraph: "No philosopher and no position is named" is checked (the
  paragraph and the post name none). I did not claim the words sequence failed to answer any
  particular question.
- The In short line calls the thermodynamic argument "sound" (for the weak claim). This agrees
  with the Second Law note, which calls "you need correlation" the uncontested half.
- Considered and dropped: a Robins-Ritov style counterexample to "every useful method is
  Bayesian" (disputed in statistics; importing it would be a general dispute and my mapping of
  it to "cognition" would be speculative).
- Typo "disguies" in the post: nitpick, not noted.
