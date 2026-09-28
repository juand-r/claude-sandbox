# Report: pretending-to-be-wise

## 1. The argument in three sentences

Just as one can overstate confidence, one can display neutrality or suspended judgment that
is not really there, in order to signal maturity, impartiality or a superior vantage point;
the author's examples are parents who say they grew out of theological questions, a
principal who says it does not matter who started a fight, and Great Powers who demand
truces. Such neutrality serves the convenience and status of the neutral party and helps
aggressors; and while suspending judgment is sometimes rational, "neutrality is a definite
judgment" that can be wrong, as is a call for compromise on abortion. One may decline to
spend limited resources on divisive issues, but should not pretend that declining, or
neutral judgment, is a mark of superior wisdom.

## 2. Sources checked

All saved in `data/sources/raz_batch1/`.

- Wikiquote, "Dante Alighieri", raw (`wikiquote_dante.txt`), Misattributed section: "The
  hottest places in hell are reserved for those who in times of great moral crisis maintain
  their neutrality. ** Henry Powell Spring in 1944; popularized by John F. Kennedy misquoting
  Dante (24 June 1963). Dante placed those who 'non furon ribelli ne fur fedeli' [were
  neither for nor against God] in a special region near the mouth of Hell". The Bartleby page
  the post links (bartleby.com/73/1211.html) and the JFK Library page were blocked (403,
  Cloudflare). I did not check Kennedy's exact wording, so the notes say nothing about it.
- "Against Maturity", LessWrong post rM7hcz67N7WtwGGjq, postedAt 2009-02-18T23:34:51Z
  (fetched via GraphQL, `against_maturity.md`). Matched: "my parents would smile and say:
  'Only children ask questions like that; when you're adult, you know that it's pointless to
  argue about it.'"; "But this is what I think my parents were thinking: If they had tried to
  answer a question as children, and then given up as adults ... they labeled 'mature' the
  place and act of giving up, by way of consolation"; also the hedge "We never really know our
  parents ... I don't know if my parents ever thought about the child-adult dichotomy when
  they weren't talking to me."
- Wikipedia, "Gaza War (2008-2009)", raw (`wiki_gaza_war_2008.txt`): "began on 27 December
  2008 and ended on 18 January 2009 with a unilateral ceasefire."
- Michael Rooney's comment on "Knowing About Biases Can Hurt People" (comment
  Z9LacBsgsH7cPAnhu, legacy id 18118, 2007-04-05, `kab_comments.json`): "... That is, where
  the rational conclusion is to suspend judgment about an issue, all too many people instead
  conclude that any judgment is as plausible as any other." The post has "when" for "where";
  no change of meaning, no note.
- Robin Hanson, "Policy Tug-O-War" (overcomingbias.com/p/policy_tugowarhtml) and "Beware
  Value Talk" (overcomingbias.com/p/the-cost-of-talking-valueshtml), `hanson_*.txt`. Matched:
  "prefer to pull policy ropes sideways. Few will bother to resist such pulls"; "arguing basic
  values often imposes large costs; such discussions threaten social norms that preserve
  group cohesion and effective conversation." These support the post's paraphrase ("the
  ability to have potentially divisive conversations is a limited resource").
- `data/originals/politics-is-the-mind-killer.md` (Posted: 2007-02-18): "If you want to make a
  point about science, or rationality, then my advice is to not choose a domain from
  contemporary politics if you can possibly avoid it. If your point is inherently about
  politics, then talk about Louis XVI during the French Revolution."

## 3. Arithmetic

- Gaza War ended 18 January 2009; post dated 2009-02-19: one month and one day ("a month
  after").

## 4. Claims about other posts

- "Belief as Attire" and "Professing and Cheering": both Posted 2007-08-02 ("from August
  2007"). The pointer in the note on "This I call" matches our notes there (no test for
  telling attire or cheering from belief).
- "Against Maturity": above. Not in Rationality: A-Z; fetched into data/sources only.
- "Politics is the Mind-Killer": above. Our Response there calls its advice an etiquette rule
  with escape clauses; my note quotes the hedge "if you can possibly avoid it" and argues only
  that this post's playground example shows the political examples were avoidable.
- "The Fallacy of Gray" (2008, later in book order): I did not repeat its criticisms. The
  note on "neutrality is a definite judgment" credits the point without comparison.

## 5. Not verified

- The Freire quotation and page (The Politics of Education, 1985, p. 122). archive.org has
  lending-only copies; search-inside was not available; Google Books quota was exhausted.
  The notes say I could not check it. The name is "Paolo" in the text and "Paulo" in the
  footnote (Paulo is correct); nitpick, no note.
- Kennedy's exact wording of the line (see above).

## 6. Judgment calls

- Note on the principal: reads the second half of the principal's sentence ("it only matters
  who ends it") as a rule addressed to the children. This is a reading of the quoted words,
  marked "Read as addressed to the children"; a commenter (Sideways2) made a related point in
  2009. I kept it because it uses the post's own quotation, not an outside hypothesis.
- \clogic after "sheer selfishness": "That a policy suits the people who follow it does not
  show that they follow it because it suits them." The post says "part of this behavior can be
  chalked up to", a partial claim; the note attacks it as unsupported, not as false.
- Note on "Against Maturity": says the earlier post explained the parents' reply as a story
  they told themselves, while this post presents it as a display. These are different
  readings, not a contradiction; I avoided "contradicts". The editor may think this is minor.
- Note on "It may be useful to initially avoid": applies "Politics is the Mind-Killer" to this
  post. The hedge "if you can possibly avoid it" is quoted, and the note says the playground
  example shows it was avoidable. Check that this is not a jab.
- Considered and dropped: a note that Rooney, later in the same thread, held that suspending
  judgment is not itself a belief ("lack of belief is not a belief"), which might seem to
  conflict with "neutrality is a definite judgment". Rooney also allowed separate beliefs
  about probabilities, so the two views may be compatible (fair-defender item 7). Dropped.
- Reserved-word flags: "wrong" only in paraphrases of the post's own "it can be wrong".
- Build: one overfull hbox (98pt) in footnote 3, caused by the post's own long URL; not in our
  notes. Converter bug: `src/new_post.py` failed on this post (md2tex.py IndexError: a link
  whose text contains an escaped underscore, footnote 3; the nested Inline object restores
  placeholders from the outer store). I built the skeleton with a wrapper that shares one
  placeholder store (`data/sources/raz_batch1/work/mk_ptbw.py`), and check_verbatim printed OK. src/md2tex.py itself was not edited.
