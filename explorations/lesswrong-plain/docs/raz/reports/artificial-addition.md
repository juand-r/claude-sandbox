# Report: artificial-addition

## 1. The argument in three sentences

In a parable, people have an evolved ability to add but do not know how it works, so
"Artificial Arithmetic" research stores lookup tables and argues over framing, learning,
evolution, emergence, computing power, brain scans, neural networks, Gödel and Searle,
while no one looks for the missing insight (which the reader knows is simple). The post
draws two morals: beware assertions you cannot regenerate from your own knowledge, and
beware dancing around confusing gaps in your knowledge instead of filling them; it says
both are shown by the real history of AI, and gives Pearl's graphical models, which
replaced the patching of non-monotonic logics, as a real case. The lesson: when the basic
problem is your ignorance, clever strategies for bypassing it fail, and "Until you know
your idea will work, it won't."

## 2. Sources checked

- Pearl 1982, "Reverend Bayes on Inference Engines: A Distributed Hierarchical Approach",
  AAAI-82 (`data/sources/pearl1982_aaai.txt`, fetched by an earlier agent from
  https://cdn.aaai.org/AAAI/1982/AAAI82-032.pdf). Matched: "Judea Pearl / Cognitive Systems
  Laboratory / School of Engineering and Applied Science / University of California, Los
  Angeles"; footnote "(**) Supported in part by the National Science Foundation, Grant IST 80
  19045."
- Kantamneni and Tegmark, "Language Models Use Trigonometry to Do Addition", arXiv 2502.00873,
  dated 2025/02/02 (`data/sources/b3a_arxiv_2502.00873.html`, abstract). Matched: "we reverse
  engineer how three mid-sized LLMs compute addition. We first discover that numbers are
  represented in these LLMs as a generalized helix"; "LLMs compute addition by manipulating
  this generalized helix"; "we present the first representation-level explanation of an LLM's
  mathematical capability."
- Cyc: Wikipedia raw (`data/sources/b3a_addition/cyc_wiki.txt`): "The project was begun in July
  1984 by Douglas Lenat"; "The Cyc knowledge base involving ontological terms was largely
  created by hand axiom-writing"; "Hoping to capture common sense knowledge".
- Penrose–Lucas argument: Wikipedia raw (`penrose_lucas_wiki.txt`): "John Lucas and Roger
  Penrose postulate that this incompleteness does not apply to humans, and conclude that humans
  can have mathematical insights that Turing machines can't. Penrose and Stuart Hameroff
  proposed a quantum explanation".
- Chinese room: Wikipedia raw (`chinese_room_wiki.txt`): "The argument was presented in a 1980
  paper by the ...".
- Stanford Encyclopedia of Philosophy, "Non-monotonic Logic" (`sep_nonmon.txt`): checked the
  post's Pearl paragraph. SEP says Pearl (1990) proposed "system Z based on ε-semantics", a
  probabilistic account of default reasoning, and that stable-model semantics from
  non-monotonic logic "serves as the foundation for the answer set programming paradigm". Not
  used in a note: it adds history but does not contradict the post, and Pearl's System Z applies
  the probabilistic insight the post praises.

## 3. Arithmetic

None.

## 4. Claims about other posts

- "Truly Part of You": `data/originals/truly-part-of-you.md`, "Posted: 2007-11-21" (this post:
  2007-11-20, so "tomorrow" fits); it opens with McDermott's "Artificial Intelligence Meets
  Natural Stupidity". Book order 48 (Map and Territory), per the manifest; our notes on it
  (annotated/afterwords/truly-part-of-you.tex) call it "Drew McDermott's 1976 critique".
- "Optimization and the Intelligence Explosion" (order 147): "natural selection is an
  *accidental* optimization process"; "humans are *optimized* optimizers handcrafted by natural
  selection".

## 5. Items not verified

- Pearl's 1988 book (the post's source) could not be read; `data/sources/pearl1988_djvu.txt` is
  a saved 401 error page. So I did not check the burglar-alarm example against Pearl, and no
  note relies on it.
- The claim that language models are trained on Web text: I dropped it from the notes (I had
  no source in hand) and say only "trained on large amounts of text".
- Whether LLM addition is reliable on large numbers: not asserted. The note says they "did
  learn to add" and that the mechanism was found in 2025 for three models.

## 6. Judgment calls for the editor

1. The later-history note on the neural-network voice (and one Response paragraph). The brief
   says predictions are not errors. This note is not a prediction check: the voice is one the
   post mocks, and the post's closing rule ("the clever ideas never work", "Until you know your
   idea will work, it won't") is a general claim that later events bear on. The note is
   phrased as information, and the Response says "the post could not have known it". The
   editor may prefer to keep only the note, or cut both.
2. The note on "Until you know your idea will work, it won't" argues from the parable's own
   premise (evolution produced human arithmetic, and one mocked voice proposes evolution). A
   fair defender could say the rule is about human research strategies within a practical time.
   The note says only that the unhedged rule sits against the premise; it does not say
   "contradicts".
3. The academia note uses "sits uneasily". Pearl's being at UCLA with NSF support shows the one
   example came from academia; it does not show academia is generally set up for such work.
   I did not use the "one paper per month" figure, which reads as hyperbole.
4. The parable note ("every voice in the list looks foolish by construction") is about the
   analogy's structure. The post anticipates the objection (fictional evidence) and answers
   with the Pearl case; the notes and Response credit that and add that the closing lesson
   claims more ("the history of previous key insights") than the one case.
5. Pronouns: "his"/"him" for Pearl and Good removed in favour of names, although both are
   historical figures.
6. Tooling incident: the main session's export at 23:55 wrote
   `annotated/notes/artificial-addition.json` (369 bytes) while my post file was briefly a bare
   skeleton (a shell loop of mine applied the wrong notes file; fixed within a minute). The
   current `annotated/posts/artificial-addition.tex` has all 23 notes; a fresh export is needed.
