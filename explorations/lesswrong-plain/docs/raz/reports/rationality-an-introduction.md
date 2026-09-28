# Report: rationality-an-introduction

## 1. The argument in three sentences

When something we value is threatened, our perceptions and reasoning rally to defend it (the
Dartmouth-Princeton game), and the stories we tell about our own reasons are often
confabulated, so we need a standard less shaky than intuition. Probability theory and
decision theory supply one: given priors and evidence there is a uniquely right degree of
belief (Bob's secret-admirer odds go from 1:5 to 2:1 after a wink), so beliefs are never a
mere matter of taste, and although we can never be perfect Bayesians the ideal lets us see
why an answer is right and where we went wrong. The book's sequences apply this to excuses,
politics, rationalization, fresh evidence, group hazards and letting go; our biases are the
substance of our reasoning, not a coating on it, but as with arithmetic we can still train
and improve.

## 2. Sources checked

All fetched files are in `data/sources/b2_intro_humility/`.

- Hastorf and Cantril (1954), "They Saw a Game". The URL in the post's footnote 1
  (www2.psych.ubc.ca/~schaller/...) now returns 404. Copy fetched from
  https://www.romolocapuano.com/wp-content/uploads/2013/06/TheySawAGame.pdf
  (`hastorf1954.pdf`, `.txt`). Matched:
  - Table 1, question 5 ("which team do you feel started the rough play?"), Dartmouth /
    Princeton students: "Dartmouth started it 36 86", "Princeton started i t 2 0" (OCR),
    "Both started it 53 11", "Neither 6 1", "No answer 3 2".
  - Text: "Although a third of the Dartmouth students felt that Dartmouth was to blame for
    starting the rough play, the majority of Dartmouth students thought both sides were to
    blame."
  - Table 2: "Dartmouth students 48 4.3* 2.7 4.4 2.8"; "Princeton students 49 9.8* 5.7 4.2 3.5".
  - Flagrant/mild: Princeton viewers "about two 'flagrant' to one 'mild' on the Dartmouth
    team"; Dartmouth viewers "about one to one when Dartmouth students judged the Dartmouth
    team". So "half" and "a third" mild are right.
  - Secondary copy also saved (`hc_sage.txt`, age-of-the-sage.org), same table.
- Mercier and Sperber (2011), abstract from PubMed 21447233 (`pubmed_21447233_mercier_sperber.txt`):
  "It is to devise and evaluate arguments intended to persuade." and "Skilled arguers,
  however, are not after the truth but after arguments supporting their views."
- Hanson, "You Are Never Entitled to Your Opinion", https://www.overcomingbias.com/p/you_are_never_ehtml
  (`hanson.txt`). The three quoted passages match word for word (title supplies "You Are
  Never Entitled to Your Opinion"; body begins "Ever! You are not even entitled to..."). The
  post's [ . . . ] omissions do not change the meaning.
- Scott Alexander, "Why I Am Not Rene Descartes", https://slatestarcodex.com/2014/11/27/why-i-am-not-rene-descartes/
  (`ssc_descartes.txt`): "Given this state of affairs, obviously it's useful to have as much
  evidence as possible, ... use a limited amount of money wisely." Matches.
- Muehlhauser, "The Power of Agency", LessWrong vbcjYg6h3XzuqaaN8, posted 2011-05-07 (GraphQL,
  `lw_power_of_agency.json`): "You are not a Bayesian homunculus whose reasoning is
  'corrupted' by cognitive biases.\n\nYou just *are* cognitive biases." Matches.
- SEP, "Bayesian Epistemology" (existing file `data/sources/sep_bayesian_epistemology.txt`),
  section 4.1: "Subjective Bayesianism is the view that every prior is permitted unless it
  fails to be coherent"; tutorial section 1.5: "there is the party of subjective Bayesians,
  who hold that every prior is permitted unless it fails to be coherent." The note quotes
  the second form. Also "This issue divides Bayesians."
- readthesequences.com, "Rationality: An Introduction" (`rts_intro.txt`): its version lists
  "'Against Rationalization' speaks to this problem, followed by 'Against Doublethink' (on
  self-deception) and 'Seeing with Fresh Eyes'". Used only to show another published version
  names the sequence, not as confirmation of any claim.
- Manifest `data/manifests/rationality_az.json`: How to Actually Change Your Mind has seven
  sequences in this order: Overly Convenient Excuses (14 posts), Politics and Rationality
  (10), Against Rationalization (14), Against Doublethink (5), Seeing with Fresh Eyes (11),
  Death Spirals (16), Letting Go (11). The LessWrong text names six.

## 3. Arithmetic

- Prior odds 1:5 (six candidates, one is Bob). Likelihood ratio 10:1. Posterior 10:5 = 2:1,
  probability 2/(2+1) = 2/3. Correct.
- Likelihood ratio vs "odds that a random winker has a crush": if a fraction c of people have a
  crush on you, the odds that a random winker has one are 10 x c/(1-c), which is 10:1 only if
  c = 1/2. Hence the note.
- Dartmouth students blaming Dartmouth at least in part: 36 + 53 = 89%. Princeton students:
  86 + 11 = 97%.
- Infractions: 9.8 / 4.3 = 2.28, "more than twice" (used only in the honest retelling).

## 4. Claims about other posts

- "Biases: An Introduction" (our notes and Response): base rate neglect is defined there
  ("grounding one's judgments in how well sets of characteristics feel like they fit together,
  and neglecting how common each characteristic is"); our Response there says the answer to
  the debiasing doubt is "one unsourced sentence and a conditional comparison". My pointer
  says only that here, too, the support is an analogy.
- "How Much Evidence Does It Take?" (order 24), our cparas: "Real questions have no known
  number of alternatives and no agreed starting probability" and "choosing it is the problem".
  My note points there instead of repeating the argument in full.

## 5. Not verified

- Pronin (2008), Vallone, Ross and Lepper (1985), Nisbett and Wilson (1977), Schwitzgebel
  (2011), Haidt (2001): not checked; the cpara on the confabulation paragraph says so. No note
  relies on them.
- Whether "Against Doublethink" was omitted from the 2015 ebook text or only from the
  LessWrong copy: I did not see the 2015 ebook.
- The ellipsis at the end of the Overly Convenient Excuses paragraph: it is in the LessWrong
  text; I do not know what, if anything, was cut. The note only reports it.

Small things left out of the notes (STANDARDS 2.4):
- "originally written by Eliezer Yudkowsky for the blog Overcoming Bias": a few posts in this
  book date from after Less Wrong opened in 2009 (the manifest has Against Rationalization
  posts up to 2009-04-07 and Against Doublethink up to 2009-03-09). Editor's slip, no note.
- Footnote 1's URL is dead (404). Not noted.
- The one overfull box in the preview (45pt) is in the post's own footnote 5 URL, verbatim
  text.

## 6. Judgment calls for the editor

1. The Dartmouth cfact ("sharper than the table"). A fair defender can say the parenthesis
   gives the "both" figure. The note grants that ("as the parenthesis says") and argues only
   that the sentence's contrast overstates the split. It could be demoted to the report if
   judged a numbers nitpick; I kept it because it changes the size of the effect the reader
   takes from the opening case.
2. The "objectively right answer" cpara says the introduction "states one side of that dispute
   as settled". The introduction's "given very modest constraints" might be read to include an
   indifference principle, which would make its claim the objective-Bayesian position; that is
   still one side of a dispute, so I think the sentence holds. Made briefly, with a pointer to
   How Much Evidence Does It Take? (STANDARDS 2.5).
3. The likelihood-ratio clogic ("Loosely worded", "the base rate neglect described in Biases:
   An Introduction"). The introduction names the likelihood ratio correctly two paragraphs
   later, and the note says so. Linking the slip to base rate neglect is my interpretation of
   what the misreading amounts to, not a claim that the author commits the fallacy.
4. "Against Doublethink" omission: put in a neutral cpara, not as a fault. Could be cut as an
   editor's slip (2.4(2)); I kept it because the paragraph's job is to list the sequences.
5. The debiasing pointer to Biases: An Introduction is a recurring criticism; made briefly.
6. Reserved-word flags ("the opposite", "wrong", "never") are all descriptive or inside the
   post's own words.
7. I considered and dropped: a note that Mercier and Sperber's hypothesis also covers
   evaluating arguments (the introduction speaks only of producing justifications, which is
   accurate for what it says); a note that "leveling up ... often means ... colliding more with
   the in-person rationality community" is unsupported (preface-like statement, 2.4(7)).
