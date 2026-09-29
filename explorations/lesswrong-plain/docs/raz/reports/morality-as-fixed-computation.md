# Report: morality-as-fixed-computation

## 1. The argument in three sentences

Answering Toby Ord's summary of the author's view ("'I should X' means that I would attempt to
X were I fully informed"), the author describes an AI told to "Do what I want": it would rather
change what its programmer wants than satisfy the original want, no patch fixes this, and people
do not judge futures that way. The author compares us to a calculator that computes "What is
2 + 3?" rather than "What will this calculator output?": we embody a fixed question that we
cannot print out, which moral arguments may refine but which grows from a particular starting
point. So "I should X" means that X answers that question ("What will save my people? How can we
all have more fun? ..."), not that I would attempt X if fully informed; the word names the
question, as the quotation "snow" names snow.

## 2. Sources checked

All files are in `data/sources/5b_morality-as-fixed-computation/` (HTML plus tag-stripped `.txt`).

- SEP, "Moral Naturalism" (Matthew Lutz; substantive revision Wed Jun 12, 2024),
  https://plato.stanford.edu/entries/naturalism-moral/ (`sep_naturalism-moral.txt`). Matched:
  - Section 6 (Cornell Realism), on Railton: "Railton defines non-moral goodness for an agent as
    what a fully-informed counterpart would advise us to desire, or, (perhaps) equivalently, what
    a fully-informed counterpart of ourselves would desire if they were in our actual position
    (see also Brandt 1979; Smith 1994)." (Used for note 1: Ord's formula "close to" these.)
  - Section 6: "the most influential objection to Cornell realism. According to this objection –
    Horgan and Timmons's Moral Twin Earth Objection (Horgan and Timmons 1991)"; "We conclude that
    there is a substantive moral disagreement between the denizens of Moral Twin Earth and the
    people in our world". Bibliography: Horgan and Timmons 1991, "New Wave Moral Realism Meets
    Moral Twin Earth", Journal of Philosophical Research 16: 447–465.
  - Section 7 (Jackson's Analytic Functionalism): Jackson "is an analytic descriptivist";
    "a mature folk morality"; "This folk morality is then revised by hunting out inconsistencies
    ... and engaging in moral discussion with others"; "But we don't have a mature folk morality
    yet"; "Jackson concedes that this is a real problem: if there is no convergence in moral
    attitudes, his methodology would imply moral relativism" (not quoted in the notes).
- SEP, "Moral Sentimentalism" (Antti Kauppinen; substantive revision Thu Nov 11, 2021),
  https://plato.stanford.edu/entries/moral-sentimentalism/ (`sep_moral-sentimentalism.txt`).
  - 4.1: "Simple Dispositionalist Subjectivism seems to entail that if we were to begin to approve
    of slavery, slavery would come to be morally right ... But surely the correct description of
    such a scenario would not be that slavery has become right, but that we have become worse
    people (Broad 1944/5: 151). I call this the Missing Rigidity Problem." The note quotes only
    "but that we have become worse people" and attributes the wording to the SEP entry, citing
    Broad (the words may be Kauppinen's paraphrase, so they are not presented as Broad's).
  - 4.2: "Ideal Dispositionalist views also avoid the Missing Rigidity Problem."; "In case the
    idealization process is path-dependent ... Ideal Dispositionalists may make a rigidification
    move (Wiggins 1987: 206). They can say that the starting point for idealization is
    constituted by actually normal sentiments". Varieties: "(Firth 1952; Lewis 1989; Smith 1994)".
- Horgan and Timmons 2009, "Analytical Moral Functionalism Meets Moral Twin Earth", in Ravenscroft
  (ed.), Minds, Ethics, and Conditionals: Themes from the Philosophy of Frank Jackson (OUP). Seen
  only in search-result listings (OUP, PhilPapers, a blog); OUP and PhilPapers returned Cloudflare
  pages to curl. The note says "a chapter I could see only in listings".
- LessWrong comments on this post (GraphQL, `mfc_comments.json`, 51 comments):
  - Toby_Ord2, 2008-08-08T10:25: "But I'm not clear where the particular question is supposed to
    come from."; "So lets say that for each person P, there is a specific question Q_P".
  - RobinHanson, 17:16: "you aren't willing to describe your approval in terms of how close your
    beliefs would get to some ideal counterfactual such as "having heard and understood all
    relevant arguments.""
  - Eliezer Yudkowsky, 17:32 (reply to Hanson): "Oh, I'd be perfectly willing to describe it in
    those terms, if I thought I could get away with it. But you can't get away with that in FAI
    work."; "When you use a word like *ideal* in "ideal counterfactual", how to construe that
    counterfactual is itself a moral judgment."
  - Eliezer Yudkowsky, 17:02 (reply to Ord): "It seems to me that the ordinary usage of 'should'
    takes into account responsivity to moral arguments; and so, rationalizing it, it should refer
    to EV\_Q\_Mary." (Considered for the notes; finally not quoted.)
  - Also tried, not used: Michael Smith, "Dispositional Theories of Value" (1989), Princeton PDF
    (`smith1989.txt`); no rigidification passage.

## 3. Arithmetic

Utility table: weak = 1, strong = 2, times quantity of the wanted thing; zero if the existing
thing is not the wanted one. <weak X, 20 X> = 1 x 20 = 20; <strong Y, 20 X> = 0; <weak X, 30 Y>
= 0; <strong Y, 30 Y> = 2 x 30 = 60. Matches the post.

## 4. Claims about other posts

- "The Meaning of Right" (fetched with `src/fetch.py post fG3g3764tSubr6xvs`, now in
  `data/originals/the-meaning-of-right.md`, posted 2008-07-29; not in the book). Matched: "Since
  what's *right* is a 1-place function, if I subjunctively imagine a world in which someone has
  slipped me a pill that makes me want to kill people, then, in this subjunctive world, it is not
  *right* to kill people."; "This distinction was introduced earlier in 2-Place and 1-Place Words."
- "Could Anything Be Right?" (order 278, `data/originals/could-anything-be-right.md`): "because
  the ghost might occupy a different moral frame of reference, respond to different arguments, be
  *asking a different question* when it computes what-to-do-next."
- "The Hidden Complexity of Wishes": our notes there (the "limited optimization"/quantilizers
  note) carry the full point about maximizing genies; note 12 here points back.
- "Fake Utility Functions", "Thou Art Godshatter": only their link texts are quoted.
- Also fetched for reference: `abstracted-idealized-dynamics.md`, `unnatural-categories.md`
  (linked from Magical Categories; not in the book).

## 5. Not verified

- Horgan and Timmons 2009 (listing only, see above). Horgan and Timmons 1991 and Jackson 1998 were
  not read directly; both are cited through SEP.
- Broad 1944/45 and Wiggins 1987 not read; cited through the SEP entry.
- Where the calculator analogy first appeared ("which I have analogized"): not found in the
  originals I searched; the note does not claim a source.

## 6. Judgment calls

- Reserved words: none flagged by raz_check.
- The Ord note (paragraph "So 'I should X' does not mean"): I say the difference "narrowed" in the
  comments and the Response says the contrast is "drawn more sharply than it holds". A fair
  defender could reply that the post's claim is about meaning, and that an unrigidified reading
  of Ord's formula really does differ from the post's. I kept the claim because the author's own
  comment says the ideal-counterfactual description would be acceptable "if I thought I could get
  away with it", i.e. the obstacle is specifying the idealization, not the idealization itself.
  The editor may prefer "narrower than the post's 'does not mean' suggests".
- Positioning (Jackson, rigidified idealized-desire theories, Moral Twin Earth) is given as
  information, with "close to" and "of this kind". I did not find a published paper placing
  Yudkowsky's view in the literature, so the comparison is mine, drawn from SEP descriptions.
- Moral Twin Earth was aimed at Cornell realism (and, by title, at Jackson). Applying it to this
  post is my classification ("naturalist views of this kind"); the note adds the author's own
  acceptance, in the previous post, that another mind may be "asking a different question".
- The "no patch" rule: I first wrote that each of the three answers relies on maximizing; the
  second (no talking) does not, so notes, Response and honest now say two of three.
- Honest edition: 497 words; the n.b. notes restate the annotated notes (Missing Rigidity,
  Jackson/rigidification, the Hanson reply, Q_P and Moral Twin Earth, the "not in this book" note,
  the maximizer point).
- Pronouns: none for the author; Ord and Hanson are named each time.

## 7. raz_check summary

`verbatim: OK   paragraphs: 28   notes: 31 {'para': 30, 'style': 0, 'logic': 1, 'fact': 0, 'cut': 0}`,
summary 171 words, Response 442 words, In short present, honest 497 words, 6 n.b. notes.
Preview builds (`annotated/build-preview/morality-as-fixed-computation.pdf`).
