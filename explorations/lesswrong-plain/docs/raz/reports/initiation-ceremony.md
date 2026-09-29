# Report: initiation-ceremony

## 1. The argument in three sentences

A story, not an argument: Brennan climbs 256 steps, is asked whether he wants to know
(yes, whatever it is), and enters a mirrored hall of hooded members of the Bayesian
Conspiracy who recite the names of dead probability theorists. The guide asks a base-rate
question; Brennan answers two-elevenths, the guide says one-sixth, the room laughs, and
Brennan, asked again, works the answer through aloud, keeps two-elevenths, and adds that
the premises seem wrong because the room holds an odd number of people. He is given the
ring and made a novice; the story stages the initiation proposed in "To Spread Science,
Keep It Secret", posted the same day.

## 2. Sources checked

Scratch folder: `data/sources/4a_initiation-ceremony/`.

- Death years, from Wikipedia raw infoboxes (`wp_Jacob_Bernoulli.txt` etc.): Jacob Bernoulli
  "1705|8|16"; Abraham de Moivre "1754|11|27"; Laplace "1827|3|5"; Edwin Thompson Jaynes
  "1998|4|30". Secondary source, used only for dates.
- The image: downloaded from https://www.lesswrong.com/static/imported/2008/03/27/elimonk2darker.jpg
  (`elimonk.jpg`, 500x423) and viewed. It shows a bearded man in a hooded brown robe with a
  white cord, in a stone tunnel, right hand raised, holding open a red and yellow book whose
  cover reads "CAUSALITY" (a second word, partly hidden, ends "...A PEARL"). I did not name
  the person or the book's author in the note.
- "You are now an initiate of the Bayesian Conspiracy.": `data/originals/an-intuitive-explanation-of-bayes-s-theorem.md`
  line 352 (book order 183).
- "Darwin Who Is Not Forgotten": `data/originals/to-spread-science-keep-it-secret.md`.

## 3. Arithmetic

Script: `data/sources/4a_initiation-ceremony/check_puzzle.py` (exact fractions). Output:
- female Virtuists 3/4 x 3/4 = 9/16; male Virtuists 1/4 x 1/2 = 1/8 = 2/16.
- P(man | Virtuist) = (2/16)/(11/16) = 2/11; odds 2:9. Brennan is right; the guide's 1/6 is not.
- Room sizes N for which 3N/4, 9N/16 and N/8 are all whole: 16, 32, 48, ... (multiples of 16);
  no odd N. Brennan's "odd number" objection is sound.
- 1/6 equals (male Virtuists)/(all women) = (1/8)/(3/4); I noted this in the script but not in
  any note, since the story gives no source for the guide's figure.
- Stairs: 16 x 16 = 256; 256 - 240 = 16 steps left at "240".
- Optics (no source, shown by reasoning): two plates of the same index with thicknesses
  t(x) and T - t(x) stacked together have total thickness T everywhere, a flat plate, so the
  distortions cancel (up to a small lateral shift). Four mirrored walls of a square room
  produce a square lattice of images, as in a kaleidoscope with four mirrors.

## 4. Claims about other posts

- "The Failures of Eld Science" (order 247, 2008-05-12): Brennan is a student of Jeffreyssai
  (lines 13, 53: ""Ah," said Jeffreyssai. "But there is a student who has not yet spoken.
  *Brennan?*""). So in book order this is Brennan's first appearance.
- "The Ritual" (order 130): the guest says "Does it not suffice that I am a domain expert,
  and you are not?" and Jeffreyssai concedes; our notes on that post describe this. Used in
  one note and the Response as a contrast of scope, not a charge.
- "Asch's Conformity Experiment" (order 116): unanimous confederates giving a wrong answer.
  Pointer only.
- "To Spread Science, Keep It Secret": same day, earlier (manifest times 05:47 and 20:40).

## 5. Items not verified

- Erin Devereux (credited for the image): not checked.

## 6. Judgment calls for the editor

1. Fiction (STANDARDS 2.2 test 3): the notes describe; none faults the story for lacking
   evidence. The Response's one limiting point is scope: the test uses a question Brennan can
   check in his head, so the harder question of when to defer is not tested; "The Ritual" is
   cited as the story where a master defers. A fair defender could say the story is about
   something else. The sentence says only "not tested here".
2. Reserved word "wrong": used for the guide's one-sixth (checked by script) and for the
   Asch confederates' answers (literal). "Since the answer is right, giving it up would be
   conformity, not honesty" is my reading of the guide's invitation; it follows the story's
   outcome (the ring is given after Brennan keeps the answer).
3. The note tying the ending to "An Intuitive Explanation" is neutral context.
4. Density: 26 \cpara notes on 54 paragraphs; the short dialogue lines and step counts have
   none. The audit does not flag them.
