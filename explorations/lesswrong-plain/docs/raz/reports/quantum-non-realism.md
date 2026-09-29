# Report: quantum-non-realism

## 1. The argument in three sentences

Physicists in the 1920s, lacking what the post calls the correct theory (many-worlds, thirty
years in the future), could at best have practised a strict "shut up and calculate": affirm
nothing the data and calculations did not force, so that no later theory would contradict them.
Instead, the post says, ignorance turned into claimed knowledge ("we don't know what the
equations mean" became "they mean nothing", "the amplitude is only a probability", "knowing the
result makes the other amplitudes zero"), and the post presses the anti-realist with "How do
you know?", arguing that "meaningless" works as a stopsign and that the equations' success is
better explained by their meaning something. The moral is that it is hard to stay in a state of
confessed confusion without inventing a story that gives closure.

## 2. Sources checked

All fetched texts are in `data/sources/4c_quantum-non-realism/` (shared with my second slug).
Exact matches were confirmed by a normalized substring search over the saved text files.

- Epigraph. Mermin, "Is the moon there when nobody looks?", Physics Today, April 1985, PDF
  from http://www.physics.smu.edu/scalise/EPR/References/mermin_moon.pdf
  (`mermin_moon_1985.txt`). Matched: "I recall that during one walk Einstein suddenly stopped,
  turned to me and asked whether I really believed that the moon exists only when I look at
  it." (cited as note 4: A. Pais, Rev. Mod. Phys. 51, 863 (1979)). Wikiquote, Albert Einstein,
  raw (`wq_einstein.txt`): same sentence, "As recalled by his biographer Abraham Pais in
  Reviews of Modern Physics, 51, 863 (1979): 907". Wikiquote lists no Bohr version. I did not
  read Pais 1979 itself.
- Pauli. Same Mermin 1985 file. Matched: "writing Born from Princeton in 1954" and "One should
  no more rack one's brain about the problem of whether something one cannot know anything
  about exists all the same, than about the ancient question of how many angels are able to
  sit on the point of a needle."
- van Fraassen. SEP "Constructive Empiricism", https://plato.stanford.edu/entries/constructive-empiricism/
  (`sep_constructive_empiricism.txt`). Matched: "Science aims to give us theories which are
  empirically adequate; and acceptance of a theory involves as belief only that it is
  empirically adequate. (1980, 12)".
- QBism. SEP "Quantum-Bayesian and Pragmatist Views of Quantum Theory",
  https://plato.stanford.edu/entries/quantum-bayesian/ (`sep_quantum_bayesian.txt`). Matched:
  "This represents no physical discontinuity associated with measurement, but merely reflects
  the agent's updated epistemic state in the light of experience."; "QBists argue that Alice,
  Bob, and any other agent can use quantum theory successfully to account for her or his
  experiences with no appeal to any physical states (hidden or otherwise) or non-local
  physical influences."; "began as a collaboration between Caves, Fuchs, & Schack at the turn
  of the 21st century (Caves, Fuchs, & Schack 2002a,b)". Objections: section 2.3 (Timpson
  2008), section 2.4 (Bacciagaluppi 2014). Also noted there: Mermin became a QBist.
- Bohr. SEP "Copenhagen Interpretation of Quantum Mechanics", https://plato.stanford.edu/entries/qm-copenhagen/
  (`sep_copenhagen.txt`). Matched: "“The entire formalism is to be considered as a tool for
  deriving predictions of definite and statistical character …” ( CC , p. 144)"; "It is
  because of the imaginary quantities in quantum mechanics ... that quantum mechanics does not
  give us a ‘pictorial’ representation"; "Bohr himself tells us that his second argument, about
  the dimensionality of configuration space, is the most important one"; "many philosophers
  have interpreted Bohr as an antirealist or an instrumentalist"; "The modern scholarly debate
  has taken Bohr to be an instrumentalist, an objective anti-realist ..., or a realist of
  various sorts"; "At Como in 1927".
- Bohm and Bell. SEP "Bohmian Mechanics", https://plato.stanford.edu/entries/qm-bohm/
  (`sep_qm_bohm.txt`). Matched: "the wave function provides only a partial description of the
  system. This description is completed by the specification of the actual positions of the
  particles"; "Bell did not establish the impossibility of a deterministic reformulation of
  quantum theory, nor did he ever claim to have done so. On the contrary, until his untimely
  death in 1990, Bell was the prime proponent ... of the very theory, Bohmian mechanics";
  "Bell showed that any hidden-variables formulation of quantum mechanics must be nonlocal".
- No miracles. SEP "Scientific Realism", https://plato.stanford.edu/entries/scientific-realism/
  (`sep_scientific_realism.txt`). Matched: "Putnam’s (1975a: 73) claim that realism “is the
  only philosophy that doesn’t make the success of science a miracle”"; "van Fraassen (1980:
  40 ...) suggests that successful theories are analogous to well-adapted organisms".
- Poll. Schlosshauer, Kofler, Zeilinger, arXiv:1301.1069, reused from
  `data/sources/4a_the-world-an-introduction/arxiv_1301.1069.txt`. Matched: "33 participants
  of a conference on the foundations of quantum mechanics"; "held in July 2011"; Question 10
  "d. Plays a distinguished physical role (e.g., wave-function collapse by consciousness): 6%".
- Mermin slogan (pointer only): see `docs/raz/reports/the-world-an-introduction.md`
  (`mermin_2004.txt`, 1989 column quoted in 2004).
- Overcoming Bias exchange (Miller, Yudkowsky): overcomingbias.com returns "Page not found";
  web.archive.org is blocked by the egress policy. Unchecked, and the note says so.

## 3. Arithmetic recomputed

- Gallant's amplitude: the rendered "−13i" is −(1/3)i, squared modulus 1/9 = 0.111. Expected
  absorptions in 1,000: 111.1; binomial SD = sqrt(1000 × 0.111 × 0.889) = 9.94; 107 is 0.41 SD
  below. "Well within chance" holds.
- Polarization: after a 90° measurement, a 45° measurement transmits with probability
  cos²45° = 0.5, and a further 90° measurement again 0.5. 47/53 in 100 is consistent with 0.5.
  The note says only "close to an even split".
- "Thirty years" from the 1920s to Everett's 1957 paper: 1927 + 30 = 1957.
- Student's "50% to 25%": a conditional probability cos²60° = 0.25 for a maximally entangled
  pair at 60°; plausible, not noted.

## 4. Claims about other posts

- "The Simple Truth" (`data/originals/the-simple-truth.md`, posted 2008-01-01): the post's
  quotation matches line 319 ("Frankly, I’m not entirely sure myself where this ‘reality’
  business comes from ... I call the former thingies ‘belief,’ and the latter thingy
  ‘reality.’"), with the middle cut and marked "…". The summary's "delegate from the court" is
  "a delegate from the Senate of Rum" in the original; not noted (nitpick).
- "Semantic Stopsigns" (posted 2007-08-24): the note only says the post applies it. That post
  also warns "No word is a stopsign of itself; the question is whether a word has that effect
  on a particular person." I did not make this a note: the post limits its scorn to a specific
  use, so it does not seem to break that caution.
- "Probability Is in the Mind" is linked from the post's own words "partial knowledge is the
  meaning of probability", which is what the QBism note quotes.
- Pointers to "The World: An Introduction" (order 184; its notes give the Mermin slogan and the
  1997 and 2011 polls) and forward to "Many Worlds, One Best Guess" (order 246, another agent).
- "Quantum Non-Realism" is cited in my notes on "If Many-Worlds Had Come First" (Huve's
  "don't exist" move, two days later).

## 5. Not verified

- The Overcoming Bias comments (see above).
- Pais 1979 itself (I rely on Mermin 1985 and Wikiquote, which agree).
- "Egan's Law ... 'It all adds up to normality'": not checked against Egan's Quarantine; no
  note depends on it.
- The QBist, Bohr and Pauli positions are given from the SEP and Mermin, not from primary texts.

## 6. Judgment calls

- The clogic on "a certainty of many worlds existing" is the main charge: the post's own rule
  against affirming what the data do not force, set against its own "certainty". It is an
  internal-consistency point, not a verdict on many-worlds. A fair defender could say the rule
  was for people without the correct theory; the note answers with "applied today" and the
  post's own present-tense "is not ruled out by the data". The editor may prefer "sits uneasily
  with" wording.
- The epigraph note ("I found no source for a question put to Bohr"): I searched Wikiquote and
  the Mermin article. It is possible Einstein asked Bohr something similar in an unrecorded
  conversation; the note says only that the documented source is Pais.
- The QBism notes (on "most embarrassing wrong turns" and on "what way could reality be"): the
  first says the mocked chain, minus the physical-vanishing step, is "close to" QBism. That is
  my comparison, based on the SEP account; a QBist would not accept "the amplitude is the
  probability" in Goofus's objective sense. I kept it because the post's verdict is the
  strongest in the text and QBism is a live, published position from 2002. I stated that the
  post argues against such readings in the Bell dialogue.
- Pauli's letter is about Einstein's realism, not about a specific photon experiment; I use it
  only as a real statement of the "meaningless to ask" stance, with its reason.
- Reserved-word flags: "contradict" (describing the post's own payoff), "never" (the post's
  "may never have happened" hedge), "wrong" (the post's "at worst wrong"), all in paraphrase of
  the post, not as charges.
- The "shut up and calculate" history note ("the order there was reversed") treats the
  post's "inside of five years" as a general prediction, so the note says the history cannot
  illustrate it, not that it refutes it.
- Honest section is 860 words, near the 900 limit for longer posts.
