# Report: the-crackpot-offer ("The Crackpot Offer", Yudkowsky, posted 2007-09-08)

## 1. The argument in three sentences (written before annotating)

At thirteen or fourteen the author thought a binary-expansion map from whole numbers to sets of whole numbers disproved Cantor's diagonal argument, found a week later that the diagonal argument itself produced a counterexample, and, after a moment of wanting to try again, saw that the failed attempt gave no reason to doubt the theorem and let it go. Holding on, or reinterpreting the error as partly right or virtuous, would have been the first step to becoming a crank. So whenever you are tempted to cling to a thought you would never have had if you had been wiser, admit that it was simply a mistake, with no hidden rightness in it, say "oops", and move on.

## 2. Sources checked

All in `data/sources/raz_batch2b/`.

- Wikipedia, "Cantor's diagonal argument" (`wiki_Cantor%27s_diagonal_argument.txt`, raw):
  "a mathematical proof that there are infinite sets which cannot be put into one-to-one
  correspondence with the infinite set of natural numbers"; "Georg Cantor published this
  proof in 1891"; "Cantor considered the set T of all infinite sequences of binary digits";
  "The uncountability of the real numbers was already established by Cantor's first
  uncountability proof, but it also follows from the above result"; "A generalized form of
  the diagonal argument was used by Cantor to prove Cantor's theorem: for every set S, the
  power set of S ... cannot be in bijection with S itself."
- Wikipedia, "Countable set" (`wiki_Countable_set.txt`): "Z (the set of all integers) and
  Q (the set of all rational numbers) are countable"; "There are only countably many finite
  sequences, so also there are only countably many finite subsets."

## 3. Arithmetic (the mathematics note must be right)

Script: `data/sources/raz_batch2b/crackpot_check.py` (run output: all checks pass).

- 13 = 8 + 4 + 1 = 2^3 + 2^2 + 2^0, binary 1101, positions {0, 2, 3} (counting from the
  right, starting at 0). Matches the post.
- The map f(n) = {positions of 1-bits of n} is one-to-one (inverse: sum of 2^i over the set)
  and its image is exactly the finite subsets of the whole numbers (every finite set S is
  f(sum 2^i, i in S)); no infinite set is in the image.
- Diagonal set D = {n : n not in f(n)}. For every n >= 0, n < 2^n, so bit n of n is 0, so
  n is not in f(n). Hence D = all whole numbers, whose "binary number" is ...1111. So the
  post's counterexample is exactly the diagonal set. Checked numerically for n < 5000 and by
  the inequality n < 2^n (true for all n >= 0).
- "the real numbers outnumber the rational numbers": follows from the diagonal argument
  (reals uncountable) plus the countability of the rationals. The note says so and calls the
  post "correct in substance, with one step left implicit."

## 4. Claims about other posts

- "The Importance of Saying Oops", posted 2007-08-05 (`data/originals/the-importance-of-saying-oops.md`);
  this post 2007-09-08: "a month earlier". The post's last line, "Say 'oops,' and get on with
  your life", matches that title. No claim about its content.

## 5. Not verified

- The book about math cranks the author read is not named; not pursued.
- The author's age (13 or 14) is the post's own account; not checkable.

## 6. Judgment calls

- The paragraph-1 `\cfact` is not a criticism; it explains what the argument shows so that
  the reader can see why a map onto sets of whole numbers bears on reals. The editor may
  judge it unneeded under 2.4(2); I kept it because the brief asked for the mathematics to be
  right and explained.
- Paragraph-6 note says "The inference is correct" (credit). Leaving it out would suggest the
  turn of the story was not sound reasoning.
- The `\clogic` on "a thought you would never have thought if you had been wiser" (the rule
  identifies its target only in hindsight) and the last-paragraph note (no way to tell mistakes
  with silver linings from those without) are two different points; both appear in the
  Response. The fair defender will say the post's subject is what to do after the mistake is
  known; the note and Response grant this explicitly ("The post's subject is what to do
  after the mistake is known, and on that subject it is clear").
- "never" appears only inside a paraphrase of the post's own phrase ("a thought you would
  never have had if you had been wiser") in the Summary.
- I did not note the drop from "thirteen or maybe fourteen" to "a child of thirteen" (nitpick).
