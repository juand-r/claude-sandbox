# Report: qualitatively-confused ("Qualitatively Confused", Yudkowsky, posted 2008-03-14)

## 1. The argument in three sentences (written before annotating)

Confusion between belief, truth and reality (as in the relativist's "different societies
have different truths") comes from thinking of beliefs as all-or-nothing, since the binary
of belief and disbelief looks like the binary of true and false. With probabilities the
types come apart: a belief is a probability in (0, 1), its accuracy is scored against
reality by the log of the probability given to what happened (a number in (-inf, 0)), and a
belief about one's own belief is usually near-certain, so calling a probability assignment
"true" is a type error. Keeping these representations distinct helps avoid the Mind
Projection Fallacy, for example the idea that a coin is itself "50% uncertain".

## 2. Sources checked

Local copies in `data/sources/4a_the-quotation-is-not-the-referent/` unless noted.

1. Wittgenstein, *Philosophical Investigations*, Anscombe translation, archive.org djvu text
   already saved by an earlier agent: `data/sources/raz_batch2_sd/wittgenstein_pi_1986_djvu.txt`
   (lines 10131-10134 and 10167-10168), Part II, section x. Matched: "If there were a verb
   meaning 'to believe falsely', it would not have any significant first person present
   indicative." (the post adds a comma after "person"); "Moore's paradox can be put like this:
   the expression "I believe that this is the case" is used like the assertion "This is the
   case"; and yet the hypothesis that I believe this is the case is not used like the
   hypothesis that this is the case." Consistent with the note on the same epigraph in
   `annotated/posts/belief-in-self-deception.tex`.
2. Wikipedia, "Scoring rule" (raw, `wiki_scoring_rule.txt`). Matched: "The logarithmic
   scoring rule is a strictly proper and local scoring rule"; "Affine functions of the
   logarithmic scoring rule are the only strictly proper local scoring rules on a finite set
   that is not binary"; "All binary scores are local"; "The Brier score, originally proposed
   by Glenn W. Brier in 1950". The note paraphrases (no quotation).
3. Dates from `data/originals/`: Qualitatively Confused 2008-03-14, Probability is in the Mind
   2008-03-12 ("two days earlier").

## 3. Arithmetic

- log2(0.7) = -0.5146 -> -0.51 (post correct).
- log2(0.3) = -1.7370 -> -1.74; the post writes -1.73 (truncation, not rounding). Too small
  to note (STANDARDS 2.4 threshold); the notes use the post's figures.
- Expectation with exact logs: 0.7(-0.5146) + 0.3(-1.7370) = -0.8813; with the post's
  rounded figures 0.7(-0.51) + 0.3(-1.73) = -0.876. Both -> -0.88. (This is the binary
  entropy of 0.7, 0.881 bits.)
- -0.51 and -1.73 both differ from -0.88, so "in neither case ... exactly as accurate as I
  expected" holds.
- log of p in (0,1) lies in (-inf, 0).

## 4. Claims about other posts

- "Probability is in the Mind" (`data/originals/probability-is-in-the-mind.md`): the coin
  example ("The coin itself has no mind, and doesn't assign a probability to anything").
- "Belief in Self-Deception": pointer to its note on the Wittgenstein epigraph.
- "Variable Question Fallacies": our note there makes the same "names or quotes none"
  point about "postmodernist professors"; the point here is about this post's own opponent.

## 5. Not verified

Nothing the notes depend on.

## 6. Judgment calls

1. The "archetypal postmodernist" note (P2) and the Response paragraph on it. An invented
   opponent is not a fault in itself (STANDARDS 2.2.4); the note's point is that the view is
   attributed to a group without anyone named or quoted. I replaced "invented" (reserved)
   with "the author's construction" in the note and "whom the post does not source" in the
   In short line. The editor may judge the point too slight for the In short line.
2. P1 note and Response: "gives no evidence about what causes the confusion". The thesis is
   hedged ("I suggest", "I hope", "perhaps"), and every mention says so.
3. I considered and dropped a note that a probability can be judged right relative to
   evidence (logical probability, calibration), so "cannot possibly be 'true'" is narrow. A
   fair reading takes "true" as "true of snow", and the objection would be my own argument.
4. Build: the official preview fails because the post's own text contains ∈ (U+2208) and ∞
   (U+221E), which the shared preamble does not declare. I did not edit the preamble. With
   `\DeclareUnicodeCharacter{2208}{\ensuremath{\in}}` and
   `\DeclareUnicodeCharacter{221E}{\ensuremath{\infty}}` added (test driver
   `annotated/build-preview/4a_test_qualitatively-confused.tex`), the post and afterword
   build with no errors and no overfull boxes. The editor should add these two lines to
   `annotated/preamble.tex`.
