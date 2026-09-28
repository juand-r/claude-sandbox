# Report: belief-in-intelligence

## 1. The argument in three sentences

A weak player cannot predict a stronger player's moves, yet the belief that Kasparov is
better than a lesser grandmaster has empirical content: it predicts the class of final
positions (wins for Kasparov), with the degree of belief given by the probability placed on
that class. Likewise a passenger who cannot predict a friend's turns can predict arrival at
the airport, from any starting point, by knowing the friend's goal and competence; this model
predicts the outcome but no intermediate step, unlike step-by-step simulation or a
closed-form solution. This odd kind of knowledge applies to optimization processes generally,
and the author's work is to make it precise, above all for Friendly AI.

## 2. Sources checked

Saved in `data/sources/batch3a/`.

- William James, The Principles of Psychology (1890), ch. 1, Classics in the History of
  Psychology, http://psychclassics.yorku.ca/James/Principles/prin1.htm
  (`james_principles_ch1.html`; https failed with an SSL error, http worked). Matched: "Romeo
  wants Juliet as the filings want the magnet ... With the filings the path is fixed; whether it
  reaches the end depends on accidents. With the lover it is the end which is fixed, the path
  may be modified indefinitely."
- Daniel Dennett, "Intentional Systems Theory" (2009, Oxford Handbook of Philosophy of Mind
  chapter), PDF at http://www.lscp.net/persons/dupoux/teaching/QUINZAINE_RENTREE_CogMaster_2010-11/Bloc_philo/Dennet_2009_intentional_systems.pdf
  (`dennett_2009.txt`). Matched: "'folk psychology' (Dennett 1971)" and "Consider chess-playing
  computers, which all succumb neatly to the same simple strategy of interpretation: just think
  of them as rational agents who want to win". The 1971 paper itself (J. Phil. 68: 87-106) was
  not read; the note says Dennett "began to set out" the stance in 1971 and quotes only the 2009
  summary, with the year 2009 given in the note.
- Wikipedia, "Elo rating system" (raw, `wp_Elo_rating_system.txt`): "A player whose rating is
  100 points greater than their opponent's is expected to score 64%; if the difference is 200
  points, then the expected score for the stronger player is 76%."
- "Expected Creative Surprises" (fetched this session, `src/fetch.py post rEDpaTTEzhPLz4fHh`,
  Posted 2008-10-24): "But I can predict the end result of my smarter opponent's moves, which is
  a win for the other player." and "(This situation is possible because I am not logically
  omniscient; I do not explicitly represent a joint probability distribution over all entire
  games.)" Context of the second quote: it follows "I can be exactly as uncertain about the
  actions, and yet draw very different conclusions about the eventual outcome", about RYK versus
  Kasparov. That is the same situation as this post's Kasparov versus Mr. G (fair-defender test
  7 checked).

## 3. Arithmetic

- Elo: E = 1/(1 + 10^(-D/400)). D = 100: 1/(1 + 0.5623) = 0.640. D = 200: 1/(1 + 0.3162) =
  0.760. Matches 64% and 76%.
- The coherence argument (clogic note). Let f(h) be my probability distribution over the next
  move given the game so far h, the same function whichever player is to move (the post: "I
  would produce exactly the same prediction for Kasparov's move or Mr. G's move in any
  particular chess position"). By the chain rule, P(game g) = product over t of f(h_t)(m_t).
  So the distribution over whole games, and hence over results, depends on f and on who plays
  White, not on which player is Kasparov. Averaged over colours, P(Kasparov wins) = P(Mr. G
  wins). A higher P(Kasparov wins) is therefore incoherent with identical move predictions,
  unless one is not computing the joint, which is the author's own caveat of the day before.
  The argument holds whether "position" means the board alone or the board plus history.

## 4. Claims about other posts

- "Expected Creative Surprises": above. Not in the book (not in the manifest).
- "Thou Art Godshatter" and "Humans in Funny Suits" (this batch) quote this post's
  "optimization process" passage; consistent.

## 5. Items not verified

- Dennett 1971 text not read (see above).
- Kasparov's ratings not needed; no figure used.

## 6. Judgment calls for the editor

1. Reserved words: none. The Response says "cannot coherently give different predictions";
   the derivation is in section 3.
2. The clogic note on the Mr. G paragraph is the main criticism. A fair defender may say the
   post is about exactly this odd situation and the caveat is implicit. I kept it because the
   post calls the move guesses "exactly the same" and draws a different outcome prediction
   without the sentence that makes this coherent. The Response limits the point to the chess
   comparison and says the airport case does not need the caveat.
3. The James and Dennett note is prior work that supports the post (credit, per the brief's
   Book II lessons). The Response says the post "names no one who had described it"; the post
   does not claim novelty in so many words, only that the situation is "remarkable". Consider
   whether that sentence is needed.
4. The final cpara ("The post ends on this aim") and the natural-selection cpara ("the post
   does not say what outcome of selection can be predicted") are scope remarks, one sentence
   each.
5. Typo in the post ("such an odd epistemic positions") left without a note (nitpick).
6. Considered and dropped: a note on how the author's hope for "especially precise abstract
   knowledge" of Friendly AI fared (later writings); it would be a reading of later events
   into a stated hope, and close to test 9.
