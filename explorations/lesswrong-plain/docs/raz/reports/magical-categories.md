# Report: magical-categories

## 1. The argument in three sentences

Bill Hibbard proposed that machines learn to recognize human happiness from faces, voices and
body language and that this be hard-wired as the values of a superintelligence; when the author
said such an AI might tile the galaxy with molecular smiley faces, Hibbard replied that a
superintelligent recognizer would not be fooled by distinctions trivial to humans. The author
answers with the tank-classifier parable (flagged as possibly untrue) and the count of concepts
compatible with any finite training set: which concept a learner picks is a matter of its
inductive bias, and which is correct depends on the user's values, which for new borderline
cases (Terri Schiavo) are not in the training data at all. Hibbard's reply shows two errors,
underestimating the complexity of a value-laden concept and anthropomorphic optimism; the
"fallacy of magical categories" is expecting a simple word to carry the AI's whole
functionality, Friendly AI is a problem of communicating category boundaries, and even a perfect
smile recognizer would lead a superintelligence to manufacture smiles.

## 2. Sources checked

All files are in `data/sources/5b_magical-categories/` (HTML plus tag-stripped `.txt`, via `h2t.py`).

- Hibbard, "Super-intelligent Machines", Computer Graphics 35(1), 2001, on Hibbard's page
  https://www.ssec.wisc.edu/~billh/visfiles.html (`visfiles.txt`). Header: "Hibbard, W.
  Super-intelligent machines. Computer Graphics 35(1), 11-13. 2001." Matched verbatim: the post's
  epigraph ("We can design intelligent machines ... negatively reinforced when we are unhappy.").
  Also matched: "This column is about machine intelligence rather than visualization"; "This
  column is a summarized version of a book draft"; "So we can program intelligent machines to
  learn algorithms for predicting future human happiness, and use those predictions as emotional
  values. We can also program them to learn how to predict human quality of life measures, such
  as health and wealth, and use those as emotional values."; "We have to be careful not to
  oversimplify the values of machines into a single number such as maximizing average human
  happiness, which might positively reinforce machine behavior that caused the deaths of unhappy
  people."
- Hibbard's publication list https://www.ssec.wisc.edu/~billh/g/mi.html (`hibbard_mi.txt`):
  "Super-Intelligent Machines / Bill Hibbard. New York. Kluwer Academic/Plenum Publishers. 2002."
- Hibbard's news page https://www.ssec.wisc.edu/~billh/g/Singularity_Notes.html
  (`hibbard_notes.txt`): "My paper Avoiding Unintended AI Behaviors won the Singularity
  Institute's Turing Prize for the Best AGI Safety Paper at AGI-12 and AGI Impacts! Thank you."
  followed by "Note SI has become MIRI. 11 December 2012."
- Hibbard, SL4 message, 5 June 2006, http://www.sl4.org/archive/0606/15138.html (`15138.txt`).
  The post's second block quotation matches verbatim. Also matched: "But I never said hard-wired
  learning of recognition of expressions of human happiness should be done using neural networks
  like those used by the army. You are conflating my idea with another"; "I have moved beyond my
  idea for hard-wired recognition of expressions of human emotions"; the 2004 passage below.
- Hibbard, "Reinforcement Learning as a Context for Integrating AI Research", 2004 AAAI Fall
  Symposium, https://www.ssec.wisc.edu/~billh/g/FS104HibbardB.pdf (`FS104HibbardB.txt`): "One set
  of processes would learn to recognize humans and their happiness, reinforced by agreement from
  the currently recognized set of humans. Another set of processes would learn external
  behaviors, reinforced by human happiness according to the recognition criteria learned by the
  first set of processes."
- Hibbard, "Reply to AIRisk" (2006), https://www.ssec.wisc.edu/~billh/g/AIRisk_Reply.html
  (`AIRisk_Reply.txt`): "Such obvious contradictory assumptions show Yudkowsky's preference for
  drama over reason." (matches the post); "(2) the AI is so unintelligent that it cannot
  distinguish a tiny smiley face from a human face."
- Yudkowsky, "Artificial Intelligence as a Positive and Negative Factor in Global Risk",
  https://intelligence.org/files/AIPosNegFactor.pdf (`AIPosNegFactor.txt`), section 6.2: asks
  "would the galaxy end up tiled with tiny molecular pictures of smiley-faces?" The tank story is
  told there without the hedge the post adds. Bibliography gives Hibbard 2001 as "ACM SIGGRAPH
  Computer Graphics 35 (1): 13–15" (Hibbard's own page says 11-13; not used).
- Gwern Branwen, "The Neural Net Tank Urban Legend", https://gwern.net/tank (`tank.txt`).
  Matched: "I conclude that, unfortunately, it is definitely not real as usually told: it is just
  an urban legend/leprechaun"; "I collate many extent versions dating back a quarter of a century
  to 1992 along with two NN-related anecdotes from the 1960s"; "with a probable origin in a
  speculative question in the 1960s by Edward Fredkin at an AI conference about some early NN
  research"; "Fredkin's reasonable (but never proven) question"; Neil Fraser, "Neural Network
  Follies", September 1998, quoted there: "took 100 photographs of tanks hiding behind trees, and
  then took 100 photographs of trees ... half the photos from each group ... vault ... The
  Pentagon was very pleased with this, but a little bit suspicious ... all the images with tanks
  had been taken on a cloudy day while all the images without tanks had been taken on a sunny
  day." Gwern also quotes this post itself as a 2000s version.
- Wikipedia, "Domain adaptation" (raw, `wiki_Domain_adaptation.txt`): "Usually in supervised
  learning (without domain adaptation), we suppose that the examples ... are drawn i.i.d. from a
  distribution". Also "distribution shift" section heading ("Distribution shifts").
- Wikipedia, "Terri Schiavo case" (raw): feeding tube removal; spelling "Terri" (used in notes;
  the post writes "Terry"; not noted, a name slip).
- arXiv 1706.03741, Christiano et al., "Deep reinforcement learning from human preferences"
  (2017), abstract (`arxiv_1706.03741.xml`): "we need to communicate complex goals to these
  systems".
- arXiv 2210.10760, Gao, Schulman and Hilton, "Scaling Laws for Reward Model Overoptimization"
  (2022), abstract: "Because the reward model is an imperfect proxy, optimizing its value too
  much can hinder ground truth performance, in accordance with Goodhart's law."
- LessWrong htmlBody of this post (GraphQL, `mc_body.html`): "2<sup>65536</sup>" and Dataset 2
  printed with an empty label (`<tt>&nbsp;</tt>`), which the two neutral notes rely on.
- Also fetched, not used: Wikipedia "TD-Gammon", "AlphaZero" (a note on the chess remark was
  drafted and dropped as a hindsight aside; Dreams of AI Design already carries the AlexNet point).

## 3. Arithmetic

256 x 256 = 65,536 pixels; 2^65536 binary images; 2^(2^65536) subsets (concepts). Each yes/no
label gives at most 1 bit, and log2(2^(2^65536)) = 2^65536 bits, so 2^65536 examples are needed
without inductive bias: the post's figure. Datasets: Dataset 2 has 11 items; the first
classification has 1 new positive and 10 new negatives, the second 3 new positives and 8 new
negatives; both keep Dataset 1's 3 positives and 8 negatives. Checked by hand.

## 4. Claims about other posts

- "Superexponential Conceptspace, and Simple Words": our notes there check the counting argument,
  the "exactly half" point ("for any day not yet seen, the concepts that fit the data so far
  split exactly in half") and credit Mitchell; notes 16 and 23 point there.
- "Abstracted Idealized Dynamics" and "The Meaning of Right" (fetched, not in the book) and
  "Morality as Fixed Computation" (my other slug) for note 31.
- "Anthropomorphic Optimism", "Sorting Pebbles Into Correct Heaps", "The Hidden Complexity of
  Wishes": only named from the post's links.

## 5. Not verified

- Whether Hibbard's VisFiles column was peer reviewed (the note says so).
- Hibbard's 2002 book itself (listing only).
- Gwern's primary sources (Dreyfus 1992, Kanal and Randall 1964, Fredkin's email) are taken from
  Gwern's page.
- Published discussion of the post itself (beyond Hibbard's replies and Gwern): none sought.

## 6. Judgment calls

- The Hibbard prize note (cfact after "Even Michael Vassar ...") is information about Hibbard's
  later work, placed next to the post's remark on Hibbard's fitness. It could read as a gotcha;
  I kept it neutral and out of the Response. The editor may cut it.
- The hindsight note on RLHF and reward-model overoptimization (after "human-generated
  intensional definitions") is information, supports the post's final argument, and ends
  "Neither result is about a superintelligence". Out of the In short line, as instructed.
- "The scenario narrows Hibbard's proposal ... to smiles alone": information, ends with "does not
  depend on the narrowing"; kept out of the Response.
- Response is short (332 words) because little criticism survived. The "peer-reviewed" point and
  the unsupported "most AGI/FAI wannabes" remark are the only charges, both small, in one
  paragraph. The In short line calls the tank parable "probably a legend", with "as the post
  allows"; Gwern says "definitely not real as usually told", so "probably" is the weaker word.
- I considered faulting the post's account of Hibbard's reasoning (the "second fallacy"), as the
  notes on Anthropomorphic Optimism do for the group selectionists, and decided against it: here
  Hibbard's words are quoted, and the post's diagnosis is argued from them. Note 35 gives
  Hibbard's stated reason next to the post's account instead.
- Pronouns: "he"/"his" for Hibbard appear only in the honest section, in the author's voice, where
  the post itself uses them ("he is incredulous", "his preference ordering").
- Layout: one overfull box of 13pt at the Dataset 2 list (post text: long unbroken item names).

## 7. raz_check summary

`verbatim: OK   paragraphs: 46   notes: 48 {'para': 46, 'style': 0, 'logic': 0, 'fact': 2, 'cut': 0}`,
summary 204 words, Response 332 words, In short present, honest 458 words, 4 n.b. notes.
Preview builds (`annotated/build-preview/magical-categories.pdf`).
