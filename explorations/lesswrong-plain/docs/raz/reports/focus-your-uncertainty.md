# Report: focus-your-uncertainty

## 1. The argument in three sentences

A TV pundit can explain any market outcome after the fact, but a novice pundit with 100
minutes to prepare excuses for bond yields going up, down or staying the same must decide
how to divide the time, and plausibility does not help, since all three outcomes are
plausible. The pundit notices that anticipation, like time and unlike explainability, is
limited: expecting one outcome more means expecting the others less, and time should follow
anticipation. Writing ironically in the voice of someone who thinks probabilities belong
only in school word problems, the post suggests that anticipation be treated as a conserved
resource to allocate, and ends by asking what an art of "focusing your uncertainty" would be
called (the implied answer is probability theory).

## 2. Sources checked

All saved in `data/sources/raz_batch1/`.

- Daniel T. Willingham, "Critical Thinking: Why Is It So Hard to Teach?", American Educator,
  Summer 2007. The post's link (aft.org/sites/default/files/periodicals/Crit_Thinking.pdf) now
  returns an HTML block page; the same PDF is at
  https://www.aft.org/sites/default/files/media/2014/Crit_Thinking.pdf (`willingham_2007.txt`).
  Matched: "people fail to use the first problem to help them solve the second: In their minds,
  the first was about vegetables in a garden and the second was about rows of band marchers";
  "If knowledge of how to solve a problem never transferred to problems with new surface
  structures, schooling would be inefficient or even futile—but of course, such transfer does
  occur." The note's summary ("people often fail to apply what they know to a problem that
  looks different on the surface") fits.
- Wikipedia, "Dempster–Shafer theory", raw (`wiki_dempster_shafer.txt`). Matched: introduced
  by Dempster (1967, "Upper and lower probabilities induced by a multivalued mapping"),
  developed by Shafer (1976); "belief about such propositions to be represented as intervals,
  bounded by two values, belief (or support) and plausibility"; "the masses of all the members
  of the power set add up to a total of 1".
- Comment by Davidmanheim, 2015-03-24, on this post (`focus_comments.json`): "There was a
  small reference to Dempster Schafer probability, ("DS") that is intended to address exactly
  this question. As Eliezer noted, you still need to divide your 100 minutes." Basis for
  "presumably" and "a commenter reads it this way".
- Stanford Encyclopedia of Philosophy, "Interpretations of Probability" (Hájek, 2023 rev.),
  https://plato.stanford.edu/entries/probability-interpret/ (`sep_probability_interpret.txt`).
  Matched: "most remarkably, Ramsey (1926) (and later, Savage 1954 and Jeffrey 1966) derives
  both probabilities and utilities from rational preferences alone"; "Ramsey shows that degrees
  of belief so derived obey the probability calculus (with finite additivity). Savage (1954)
  likewise derives probabilities and utilities from preferences". Bibliography: "Ramsey, F. P.,
  1926, 'Truth and Probability'"; "Savage, L. J."

## 3. Arithmetic

- Log payoff. Maximize E = sum_i p_i ln t_i subject to sum_i t_i = 100, t_i > 0 (p_i sum to 1).
  Lagrangian: dE/dt_i = p_i / t_i = lambda for all i, so t_i = p_i / lambda. Summing:
  100 = (sum p_i) / lambda = 1 / lambda, so lambda = 1/100 and t_i = 100 p_i. The objective is
  concave, so this is the maximum. (The base of the logarithm does not matter.)
- Linear payoff: E = sum_i p_i t_i is maximized by putting all 100 minutes on the i with the
  largest p_i (a linear function on the simplex is maximized at a vertex).
- Other concave payoffs do not give proportionality, e.g. sqrt: p_i / (2 sqrt t_i) = lambda
  gives t_i proportional to p_i^2. Not stated in the note (the note says only "With other
  assumptions the match fails", then gives the linear case).

## 4. Claims about other posts

None.

## 5. Not verified

- Nothing the notes rely on. The post shifts from "bond yields" (first paragraph) to "bond
  prices" (sixth, eighth). Yields and prices move in opposite directions, so "up" means
  different things, but the argument is unaffected; I judged it a slip with no consequence
  (STANDARDS 2.4(2)) and made no note.

## 6. Judgment calls

- The post is mostly irony. I did not criticize any ironic sentence as a claim (for example
  "Alas, no one can possibly foresee the future" or "the relation can't actually be
  quantified"); the notes describe them as irony.
- \clogic on the log-utility parenthesis: a technical claim (proportional allocation only
  under log payoff). Derivation above. The note does not say the post is wrong; it says the
  step rests on the assumption and sits in an aside.
- \clogic on "DS": identification is marked "presumably" and supported by a commenter. The
  claim that a fixed budget does not by itself exclude Dempster–Shafer rests on the
  normalization of mass functions (Wikipedia). The note does not say probability is not the
  better choice; the Response says "The post may be right to prefer probabilities".
- Last note: names Ramsey and Savage as the literature the post's question points to. No charge
  of uncredited borrowing, since the post does not claim the idea as new; it is information.
