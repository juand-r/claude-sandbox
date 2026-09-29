# Report: fake-utility-functions

## 1. The argument in three sentences

People who propose one simple utility function for a superintelligence (for example
"complexity") propose it too fast, partly misled by the author's old word "supergoal";
but human values are many and not derived from one another (a "thousand shards of desire",
as evolutionary psychology describes), so leaving out even one, such as the value of
running one's own life, could produce a catastrophe. Such proposers defend their principle
by pointing to its good consequences ("a superintelligence maximizing complexity would
encourage mothers to love their children"), which is motivated stopping, since a real
complexity maximizer would look for something more complex, and a fake morality, since
justifying the principle by its consequences shows that the consequences are what is really
valued. Only your morality reliably reproduces the decisions your morality would make, so a
human morality cannot be compressed into a simple utility function, any more than a large
file can be compressed into 10 bits.

## 2. Sources checked

All new files are in `data/sources/5a_fake-selfishness/`.

- Yudkowsky, Creating Friendly AI 1.0 (2001), https://intelligence.org/files/CFAI.pdf
  (`cfai.pdf`, `cfai.txt`). Glossary matched: "supergoal content. The root of a directional goal
  network. A goal which is treated as having intrinsic value, rather than having derivative value
  as a facilitator of some parent goal." Plural use, e.g. "even if the supergoals are absolutely
  constant". "supergoal" occurs 341 times.
- Nick Bostrom, "Existential Risks" (2002), https://nickbostrom.com/existential/risks.html
  (`bostrom_risks.html`, `.txt`). "hyperexistential" and "worse than death" do not occur (checked
  case-insensitively). Matched: "Flawed superintelligence Again, there is the possibility that a
  badly programmed superintelligence takes over and implements the faulty goals it has erroneously
  been given." (The current page has updated reference URLs; the section text is the 2002 text as
  far as I can tell. Not compared with a 2007 copy, since web.archive.org is blocked.)
- Wikipedia, "With Folded Hands ..." (`?action=raw`, `wiki_with_folded_hands.txt`). Matched:
  "is a 1947 science fiction novelette", "first appeared in the July 1947 issue of Astounding
  Science Fiction", Prime Directive: "to serve and obey and guard men from harm".
- SEP, "Value Pluralism" (substantive revision Sun Jun 4, 2023),
  https://plato.stanford.edu/entries/value-pluralism/ (`sep_value-pluralism.txt`). Matched:
  "Pluralists argue that there really are several different values, and that these values are not
  reducible to each other or to a supervalue."; "Ross, by contrast, is a pluralist ... (See Kant
  (1948), Ross (1930).)"; "Monist utilitarians must claim that all other putative values, such as
  friendship, knowledge and so on, are only instrumental values". Note: the quoted definition in the
  note begins "that there really are", taken from "Pluralists argue that there really are".
- Mill, Utilitarianism, ch. 4, Project Gutenberg #11224 (`gut_11224.txt`, line 1536): "if human
  nature is so constituted as to desire nothing which is not either a part of happiness or a means
  of happiness". The note quotes the phrase from "desire nothing".
- The About.com link (atheism.about.com/library/FAQs/phil/blfaq_phileth_cat.htm): host does not
  resolve; web.archive.org is blocked. The note says only that the page is no longer online.

## 3. Arithmetic

None. (The "10 bits" comparison is an analogy; no computation.)

## 4. Claims about other posts

- "Fake Fake Utility Functions" (fetched with `src/fetch.py post D6rsNhHM4pBCpDzSb` to
  `data/originals/fake-fake-utility-functions.md`; not in the book). Matched: "'happiness' is one of
  the Fake Utility Functions I run into more often" and "to avoid the Fake Utility Function of
  'genetic fitness'"; it lists as prerequisites "Fake Selfishness", "Fake Morality", "Fake
  Optimization Criteria", "Thou Art Godshatter" and others. Posted 2007-12-06 06:30 UTC; this post
  2007-12-06 16:55 UTC. "Yesterday" fits US time; not noted.
- "Hold Off on Proposing Solutions" (`data/originals/hold-off-on-proposing-solutions.md`): both
  quotations match (Maier's edict; Dawes: "I have often used this edict with groups I have
  led—particularly when they face a very tough problem, which is when group members are most apt to
  propose solutions immediately."). Our notes there discuss the unverified Dawes book; this post
  points back only.
- "Thou Art Godshatter": "splintered into a thousand shards of desire" (original). Our Response
  there: "The central step is an inference presented as history." The FUF Response quotes that
  description.
- "Adaptation-Executers, not Fitness-Maximizers", "Evolutionary Psychology": pointed to, not
  repeated (Mayr, Tooby and Cosmides are made there).
- "Fake Justification": the million-dollar laptop test ("But it would be even *more* efficient to
  buy 5,000 One Laptop Per Child laptops"); our Response there makes the unnamed-people point
  ("claims about the inner states and histories of unnamed people, and the post gives no case"),
  pointed to from P11.
- "Fake Morality" (my batch): last line "Whichever one *actually* holds open doors for little old
  ladies." cited in the "it means" clogic.
- "Not for the Sake of Happiness (Alone)" is annotated by another agent; I refer to the post only
  in passing, not to its notes. (The final P16 note no longer names it.)

## 5. Not verified

- Whether any real person proposed "complexity" as a superintelligence's utility function. The
  post gives no source; the notes say so.
- The Maier and Dawes material (see the Hold Off report).

## 6. Judgment calls

- The "it means" clogic (P14) uses the post's own next paragraphs (affective death spiral,
  "sell a lot more bananas") and the linked Fake Morality ending. It says "stronger than", not
  "contradicts". It is kept out of the In short line since the post's main point survives it.
- P8: "known fact" with no evidence in the post beyond earlier posts. A defender could say the
  seventh paragraph's links to Godshatter are the evidence; the note says the support is "the
  evolutionary account of the earlier posts", which grants that.
- P11: claims about unnamed proposers; the post reports its own experience ("I run across more of
  these people than you do"), so the note does not doubt that such people exist, only notes that
  the evidence for what they know is one unsourced reply.
- The Bostrom note is information (the term is not Bostrom's). The editor may judge it a nitpick;
  I kept it because a reader following the link would look for the word.
- P16 credits the post: its requirement for a monist matches SEP's statement. Mill is information
  that monists attempt the argument the post asks for; not a fault.
- Addendum note: scope sentence (whether a superintelligence should serve human values as they
  are is not argued here). The addendum itself defers this, so it is scope, not a fault.
- Reserved "wrong" appears only in the post's phrase "fast wrong solution". "inference" flag is
  the Godshatter notes' own description, not a motive reading.
- Honest section is 517 words, slightly over 500.
