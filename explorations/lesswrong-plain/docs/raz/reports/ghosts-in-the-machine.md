# Report: ghosts-in-the-machine

## 1. The argument in three sentences

The common objection that a self-modifying AI will "just remove any constraints" imagines a
ghost inside the machine that reads the program and decides whether to obey; but there is
no ghost, and any decision the AI makes, including one to rewrite itself, is the lawful
result of the code it started with (plus the sensory dependencies built into that code).
So a Friendly AI is not a selfish AI with a conscience bolted on: you build the conscience
and that is the AI, and conversely nothing that seems obvious to you will happen inside the
machine unless you built the causes of it, which is why AI is harder than people imagine.
Deep Blue shows that this does not mean programming each decision: it played better than
its programmers, but only through a chain of causes that began in their code.

## 2. Sources checked

- RinkWorks, "Computer Stupidities: Programming", http://rinkworks.com/stupid/cs_programming.shtml
  (curl; `data/sources/b3a_ghosts/cs_programming.html` and `.txt`). All three stories are
  there. The first two match the post word for word ("A few of them didn't understand that
  computers are not sentient", "How else is the computer going to understand what I want it to
  do?"; "10 Preheat oven to 350 / 20 Combine all ingredients in a large mixing bowl / 30 Mix
  until smooth"). The third story's prose and dialogue match ("It's logical what the right
  solution is, and the computer should reorder the instructions the right way"), but the
  program differs in small ways: the site has `readln`/`writeln`, `:=`, semicolons, and a
  second bug, `c_total := carrots + c_price`; the post has `read`/`write`, `=`, and
  `carrots * c_price`. The site may have been edited since 2008, or the post simplified it. The
  difference does not change the point; the note says "in nearly the same words; only the
  third program's code differs in small details".
- Stephen M. Omohundro, "The Basic AI Drives",
  https://selfawaresystems.files.wordpress.com/2008/01/ai_drives_final.pdf (pdftotext;
  `data/sources/b3a_ghosts/omohundro2008.txt`). Matched: "There are an endless number of ways
  to circumvent internal restrictions unless they are formulated extremely carefully." Also
  relevant, not quoted: "These potentially harmful behaviors will occur not because they were
  programmed in at the start, but because of the intrinsic nature of goal driven systems." The
  PDF has no date or venue in its text; its URL path is 2008/01 and its creation date is 25
  January 2008. I believe it appeared in the proceedings of the first AGI conference (2008) but
  could not confirm the venue (Semantic Scholar rate-limited; Crossref lists only later
  reprints). The notes say only "(2008)" and "the same year".
- Ouyang et al., "Training language models to follow instructions with human feedback",
  arXiv 2203.02155, dated 2022/03/04 (`data/sources/b3a_arxiv_2203.02155.html`, abstract meta
  tag). Matched first sentence: "Making language models bigger does not inherently make them
  better at following a user's intent."
- "The Ultimate Source": LessWrong GraphQL `EsMhFZuycZorZNRF5`, postedAt 2008-06-15T09:01:41Z
  (`data/sources/b3a_ghosts/the_ultimate_source.md`). Definition used in the note: "To have
  Author* self-control is not only have *control* over your entire existence and past, but to
  have *initially written* your entire existence and past, without having been *previously*
  influenced by it".
- "Grasping Slippery Things": LessWrong `HnS6c5Xm9p9sbm4a8`, postedAt 2008-06-17T02:04:58Z
  (this post: 2008-06-17T23:29:17Z, so "earlier the same day" holds in UTC).
- Neither post is in `data/manifests/rationality_az.json` (checked by slug).
- Ryle's phrase "ghost in the machine" (Wikipedia raw, `data/sources/b3a_ghosts/ryle_wiki.txt`):
  checked but not used; a commonplace phrase needs no credit (STANDARDS 2.2 test 4).

## 3. Arithmetic

None.

## 4. Claims about other posts

- "The Ultimate Source" (15 June 2008) and "Grasping Slippery Things" (17 June 2008): dates and
  absence from the book, above.
- "Friendly AI" is not glossed in this post, but "Minds: An Introduction" (order 131) defines
  Friendly AI theory, so I made no note on it.

## 5. Items not verified

- The venue of Omohundro's paper (see above).
- Deep Blue's strength relative to its programmers is the post's claim; I did not check it,
  since no note disputes it.

## 6. Judgment calls for the editor

1. The main note (on the "A Friendly AI is not a selfish AI" paragraph): the objection has a
   version with no ghost, and the post's positive answer grants that version for AIs built as
   goals plus constraints. I checked that this is not a "never answers" charge: the note says
   the paragraph is the post's answer. The claim is that the ghost diagnosis fits only some
   objectors. Omohundro is cited as a contemporary statement of the ghost-free version; his
   quote concerns restrictions on self-improvement, a case of the general point, not the exact
   Friendly AI objection.
2. The note on the stories ("the post does not show that the people who raise the objection
   do [think this way]") is a scope point. A fair defender could say the stories only
   illustrate. I kept it because the post's opening questions treat the objection as the ghost
   error and the stories are the only evidence offered for that error.
3. The language-model note is information, and it supports the post (instruction following had
   to be trained). It is not a prediction check.
4. I did not note "If you have a program that computes which decision the AI should make,
   you're done": it is conditional (Book II lesson on conditional claims).
5. Layout change to the skeleton, for the editor to confirm: I removed the four `-{}--` lines
   inside the quote. They are the original's `> ---` horizontal rules between stories;
   `md2tex.py` keeps them as text inside block quotes, while `check_verbatim.py` strips `---`
   lines from the original, so the fresh skeleton failed the verbatim check (4 inserted `---`).
   I also added `\\` line breaks where the original has Markdown hard breaks (the two program
   listings and the Me/Him dialogue), so the programs print one statement per line. No word
   changed; `check_verbatim.py` prints OK. A permanent fix would be in md2tex (drop `---` inside
   quotes) and would regenerate this skeleton; I did not touch the tools.
6. "Author* source" note is a \cstyle on reader cost; the post links the term, but the book's
   reader has no link to follow.
