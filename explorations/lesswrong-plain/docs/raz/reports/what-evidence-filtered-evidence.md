# Report: what-evidence-filtered-evidence

## 1. The argument in three sentences

When a clever arguer reports only true facts but chooses which to report, what you should
condition on is not the facts alone but the event that a speaker following some selection
rule said them; the coin and Monty Hall examples show that the same words support very
different conclusions under different rules. Adversarial procedures, in which each side
presents the evidence the other omits, can come close to one honest inquirer for two-sided
questions, but not for many-sided ones. The idea of filtering must not become an excuse to
dismiss evidence you dislike: if you already know your own side's case, a contrary fact is
still evidence, and only a one-sided argument heard for the first time calls for extra
caution.

## 2. Sources checked

- Jaynes, *Probability Theory: The Logic of Science*, ch. 1 (`data/sources/jaynes_book_ch1-3.txt`,
  already in the repo, lines 1456-1460): desideratum (IIIb) "The robot always takes into
  account all of the evidence it has relevant to a question. It does not arbitrarily ignore
  some of the information". Note quotes "always takes into account all of the evidence it
  has relevant to a question". The post's "on pain of paradox" was not checked.
- Author's comment, 2007-09-30, id oc9f4mNpBmcWEKQAS (`data/sources/b2_againstrat/comments_wefe.json`,
  GraphQL): "Your actual probability starts out at 0.5, rises steadily as the clever arguer
  talks (starting with his very first point, because that excludes the possibility he has 0
  points), and then suddenly drops precipitously as soon as he says "*Therefore...*""
  Note omits the parenthesis with \ldots. "he" is inside the quotation (the comment's
  pronoun for the arguer), flagged by raz_check.
- Wikipedia, "Inquisitorial system" (raw, `wiki_inquisitorial.txt`): "It is the prevalent
  legal system in [[Continental Europe]], Latin America, African countries not formerly
  under British rule, East Asia (except Hong Kong), Indochina, Thailand, and Indonesia."
  Also: "An inquisitorial system is a legal system in which the court, or a part of the
  court, is actively involved in investigating the facts of the case." The article carries
  a "Refimprove" banner; cited as Wikipedia. It also says the adversarial/inquisitorial
  distinction is "theoretically unrelated" to the civil/common-law distinction; my note
  says "adversarial systems of common-law countries", which is the usual pairing, not an
  identity.

## 3. Arithmetic

- H-biased coin 2/3 vs T-biased 1/3, equal priors. Likelihood ratio per head 2, per tail 1/2.
  - Rule 1 (report flips 4, 6, 9 regardless): three heads, odds 2^3 = 8:1. Post: 8:1. OK.
  - Rule 2 (report all heads): 3 H, 7 T: 2^3 / 2^7 = 1/16. Post: 1:16. OK.
  - Rule 3 (report only if P(H-biased) > 98%): odds > 49 needs 2^(h - t) > 49, i.e.
    h - t >= 6 (64); with h + t = 10, h >= 8. Posterior odds >= 2^6 = 64:1. The note says
    "at least 8 of the 10 flips were heads, odds of 64 to 1 or more." (Strictly the listener
    knows only that the posterior exceeded 98%, i.e. h >= 8, so the odds given the report are
    a mixture over h = 8, 9, 10, each >= 64:1.)
- Monty Hall: standard host, switching wins with probability 2/3; host always opens door 2:
  given door 2 empty, P(1) = P(3) = 1/2; host opens only when you picked the money: stick
  wins with certainty. All as in the post.
- Bits: log2(2/3 / 1/3) = 1, the text's "1 bit". The footnote's definition, -log2 p, is
  information; see our note on "How Much Evidence Does It Take?" for the same switch.

## 4. Claims about other posts

- "The Bottom Line", Posted 2007-09-28; this post 2007-09-29 ("the day before").
- Our note on The Bottom Line's key step (`annotated/posts/the-bottom-line.tex`) says "The
  right conclusion is 'discount for selection,' not 'ignore.' Yudkowsky makes this very
  point the next day, in 'What Evidence Filtered Evidence?' ... 'Each statement that the
  clever arguer makes is valid evidence.'" My first note agrees.
- Parallel worlds pointer: our note on The Bottom Line ("The many-worlds picture is not
  needed ..."). Made briefly here, per STANDARDS 2.5.
- Bits pointer: our note on "How Much Evidence Does It Take?" ("This defines the information
  in an outcome ... The reader is taught one measure and then asked to add up another.").
- Our "Rationalization" notes (next day) say the prosecutor/defender concession there is
  not answered in that post. This post's many-sided qualification ("But that is with two
  boxes...") is an answer given one day earlier. I did not note this here; the editor may
  want to add a pointer in "Rationalization".

## 5. Not verified

- "on pain of paradox" (Jaynes) not traced.

## 6. Judgment calls

- cfact "'Most' is overstated": rests on Wikipedia (flagged refimprove). The claim is about
  the number of legal systems, and civil-law/inquisitorial systems cover most of the
  world's jurisdictions by the article's list. Many systems are mixed; "overstated", not
  "false".
- clogic "Assumed, not argued" on "If you're ticked off ... then you are familiar with the
  case": the post states it unhedged; the following sentence has "probably". I attack only
  the unhedged sentence.
- clogic that the post "does not work through its opening case": the post does return to
  the box (two arguers; "a blue stamp on box B is still evidence"), so I avoided "does not
  return" and said it does not work the single-arguer case through. The author's comment is
  credited.
- Response credits the post as the answer The Bottom Line needed; consistent with our
  Bottom Line notes.

## 7. Markup change to the skeleton (not a text change)

`new_post.py` produced a skeleton that failed `check_verbatim.py`: the post's footnote 1 has
two paragraphs, and the converter put the first in a `\cauthor{}` at the marker and left
the second ("Suppose a question has exactly two possible ...") as a body paragraph at the
end, so the word order differed from the original. I moved the second paragraph into a
second `\cauthor{}` immediately after the first. No character of the text changed;
`check_verbatim.py` prints OK. `src/md2tex.py` may split other multi-paragraph footnotes the
same way.
