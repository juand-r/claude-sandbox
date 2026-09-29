# Report: Value is Fragile (batch 5b, order 285)

## 1. The argument in three sentences

The post states, as a conclusion whose argument lies in the author's earlier posts, that a
future not shaped by goals which inherit human values in detail and reliably "will contain
almost nothing of worth." It illustrates this with three minds that each lack one part of
human value (boredom; the real objects of feelings; conscious experience), argues that
boredom is an evolved human algorithm rather than something every optimizer shares, and
calls value "fragile" because losing any one of several such parts loses almost everything.
It answers the "cosmopolitan" who would let the future go its own way: the wish for a
strange and wonderful future is itself a human value, so without human values steering, the
result is "moral noise," a universe tiled with paperclips.

## 2. Sources checked

All saved in `data/sources/5b_value-is-fragile/` unless stated.

- Comments on the post, LessWrong GraphQL API (`comments.json`, 109 comments, view
  postCommentsOld, post id GNnHHmm8EzePmKzPk).
  - Robin_Hanson2, 2009-01-29, comment vrGkpxx2t2XobdMuZ: "I have read and considered all of
    Eliezer's posts, and still disagree with him on this his grand conclusion. Eliezer, do you
    think the universe was terribly unlikely and therefore terribly lucky to have coughed up
    human-like values, rather than some other values?" Notes quote "read and considered all of
    Eliezer's posts", "grand conclusion", "terribly lucky to have coughed up human-like values".
  - Eliezer Yudkowsky, 2009-01-29, comment EEqYW4u89ruyMQYzQ (reply to Hanson): "We're judging
    the winding path that evolution took to human value, and judging it as *fortuitous* using
    our human values." Note quotes "using our human values"; the note's "fortunate" is a
    paraphrase of "fortuitous".
  - Eliezer Yudkowsky, 2009-01-29, comment DmxvzsxqbW7ZLYG7w: "(B) Having a human idiom of
    boredom that desires a steady trickle of novelty: MEDIUM." (for an evolved alien species).
- Katja Grace, "Counterarguments to the basic AI x-risk case", AI Impacts, 2022,
  https://aiimpacts.org/counterarguments-to-the-basic-ai-x-risk-case/ (`grace.html`,
  `grace.txt`, fetched with curl). Matched: "This sounds to me like ‘value is not resilient to
  having components of it moved to zero’, which is a weird usage of ‘fragile’, and in
  particular, doesn’t seem to imply much about smaller perturbations." The note's "reads like"
  paraphrases "sounds to me like"; the subject of "doesn't seem to imply" is the argument, as in
  the note.
- Erik Jenner and Johannes Treutlein, "Response to Katja Grace's AI x-risk counterarguments",
  LessWrong, 19 Oct 2022, post GQat3Nrd9CStHyGaq (`response_grace.json`, `response_grace.md`).
  Matched: "human values are not fragile to $\varepsilon$-perturbations, but they are fragile to
  the mistakes we actually expect the objective to contain, such as conflating "the actual
  state of the world" and "what humans think is the actual state of the world"."
- M. Brezzi and T. L. Lai, "Optimal learning and experimentation in bandit problems", Journal
  of Economic Dynamics & Control 27 (2002) 87-108,
  http://www-stat.wharton.upenn.edu/~steele/Courses/900/Library/Bandits/BrezziLai02.pdf
  (`brezzilai02.pdf`, `brezzilai02.txt`). Matched (pdftotext line 666 f.): "a simple proof of the
  incomplete learning theorem for k-armed bandits with k ≥ 2: With positive probability, the
  optimal rule chooses the optimal action only a finite number of times" (pdftotext renders
  "finite" as "0nite", a ligature). "This generalizes the results of Rothschild (1974), McLennan
  (1984) and Banks and Sundaram (1992)." On patience: "as β (= e^{-c}) → 1 ... suggesting
  continued experimentation with aj" (β is the discount factor), which the note gives as "the
  more heavily the agent weighs the future, the more the optimal rule experiments", with
  "suggests".
- G. E. Moore, Principia Ethica, sec. 50, from the copy another agent saved at
  `data/sources/5a_ends-an-introduction/moore_principia.txt` (lines 4058-4083). Sidgwick as
  quoted by Moore: "No one ... would consider it rational to aim at the production of beauty in
  external nature, apart from any possible contemplation of it by human beings." Moore: "The
  only thing we are not entitled to imagine is that any human being ever has or ever, by any
  possibility, can, live in either"; "Certainly I cannot help thinking that it would". The notes
  paraphrase only; no Moore words are quoted.
- "Invisible Frameworks" (2008), fetched with `src/fetch.py post sCs48JtMnQwQsZwyN` to
  `data/originals/invisible-frameworks.md`. Matched: "the metamoral argument "Many agents will do
  X!" is sufficient for Roko to adopt X as a terminal value".
- "In Praise of Boredom" (posted 2009-01-18), `src/fetch.py post WMDy4GxbyYkNrbmrs` to
  `data/originals/in-praise-of-boredom.md`. Matched: "Evolved aliens might, or might not,
  acquire roughly the same boredom in roughly the same way." Its exploration/exploitation
  argument ("It wouldn't be *boring,* just maximally instrumentally efficient") is the one the
  post points to.
- Also fetched for reading: "The Fun Theory Sequence" (K4aGvLnHvYgX9pZHS) and "Lawful
  Creativity" (KKLQp934n77cfZpPn), both to `data/originals/`.
- Checked and not used: Hans Moravec's "mind children" (search summaries only; the quoted
  line says the machines "share our goals and values", so it is not a clean example of the
  "cosmopolitan" view and was dropped).

## 3. Arithmetic

- "eleven days earlier": In Praise of Boredom posted 2009-01-18, this post 2009-01-29:
  29 - 18 = 11.
- "For the third time": "75%" appears in three paragraphs of the post, those beginning
  "And I'm not going to iterate", "And then there are the long defenses" and "And so on and so
  on". Counted with grep: 3 lines.
- Fun Theory posts in the book: matched each title in the Fun Theory Sequence index against
  the manifest; only Sympathetic Minds (282), High Challenge (283), Serious Stories (284).

## 4. Claims about other posts

- Fake Utility Functions, `data/originals/fake-utility-functions.md`: "the complicatedness of
  human morality is a *known fact.*" Our note there says the claim is asserted, supported by the
  earlier evolutionary posts; my pointer only sends the reader there.
- High Challenge, `data/originals/high-challenge.md`: "There must be the true effort, the true
  victory, and the true experience—the journey, the destination and the traveler."
- Not for the Sake of Happiness (Alone): "I value freedom" (original); our notes there carry
  Nozick, Moore and Sidgwick in full, so here I only point back (STANDARDS 2.5).
- No Universally Compelling Arguments: our notes carry Bostrom's orthogonality thesis and Kant
  (review_log batch 5a: "The orthogonality thesis is stated in No Universally Compelling
  Arguments"). Pointer only.
- The True Prisoner's Dilemma (order 281) uses the paperclip maximizer (original, line 70 f.);
  so do Detached Lever Fallacy (267) and Morality as Fixed Computation (279).
- The Gift We Give To Tomorrow (286): its notes (original edition) take up Street's debunking
  argument. My notes do not repeat that; they only cite the author's reply to Hanson, which
  points to that post. Consistent with its notes.
- The book order and dates are from `data/manifests/rationality_az.json` and the Posted lines.

## 5. Not verified

- Rothschild (1974), McLennan (1984), Banks and Sundaram (1992) and Brezzi and Lai (2000) were
  not read; the theorem is cited as stated in Brezzi and Lai (2002).
- The Stanford technical report page for Brezzi and Lai (2000) had no abstract.
- Grace's essay has a later AI Impacts blog copy; I used the aiimpacts.org page only.

## 6. Judgment calls for the editor

- Reserved word: the only flag is "wrong" in a cpara that paraphrases the post's ironic voice
  ("notice that its utility function was wrong"). Kept.
- "Sits uneasily" (the no-free-lunch rule against the post's own account of evolution). The
  author can answer that the evolutionary origin is the "moral miracle", improbable and not to be
  relied on; I give that answer (via the reply to Hanson) in the same note, and the note does not
  say "contradicts". It is also in the Response and "In short". Please check that it passes the
  fair-defender test; the unhedged rule "Valuable things appear because..." is what it targets.
- "In short" also says the examples show removal, not "the lesser disturbances it also warns
  of". The post does say "or even *disturbed* in the wrong dimension" and "Touch too hard in the
  wrong dimension"; all three examples remove a dimension. Grace (2022) is later and concerns AI
  training, so she is named only in the notes and Response, not in "In short".
- The "alone" note (L61) is a slip whose point survives; kept in notes and one honest n.b.,
  out of the Response and "In short".
- Two credit points in the Response (the bandit result; the reply to the cosmopolitan being
  coherent on its own terms). Could be trimmed to one if the editor prefers.
- Neutral book-selection note on "In Praise of Boredom" (not in the book). Informational only.
- The cstyle gloss of "metamorals" quotes a post outside the book; could be cut as a jargon note.
- No "My reading" inferences. Pronouns: Hanson is referred to by name only.
- Honest section is 512 words (limit about 500). Summary 179 words (about 150): the post has
  three examples plus a boredom argument plus a conclusion; could be trimmed.
