# Report: the-parable-of-the-dagger

## 1. The story's point in three sentences

A short story, not an argument: a jester sets the king a two-box puzzle whose inscriptions
refer to each other's truth, adds a rule ("one, and only one, of the inscriptions is true"),
and the king, who does not reason it out, is bitten by a frog. The king then sets the jester
a two-box puzzle with a self-referring inscription and no rule about truth; the jester reasons
validly that the key must be in the second box and finds the dagger there. The king's closing
line gives the moral: he merely wrote the inscriptions and put the dagger where he liked, so
writing on a box does not decide what is in it (adapted, as the post says, from Smullyan).

## 2. Sources checked

Saved in `data/sources/b3b_the-parable-of-the-dagger/`.

- Smullyan, *What Is the Name of This Book?* (Copyright 1978), full text from archive.org
  (`https://archive.org/download/WhatIsTheNameOfThisBook/What-is-the-Name-of-this-Book_djvu.txt`,
  saved as `smullyan_wintb_djvu.txt`). Matched:
  - Problem 70, "D. The Mystery: What Went Wrong?": two caskets, silver and gold; the suitor
    reasons "the portrait must be in the gold casket" and "To his utter horror the gold casket
    was empty"; Portia opens the silver: "Sure enough, the portrait was there."
  - Solution 70: "The statement on the gold casket, "The portrait is not in here,""; the silver
    casket said "Exactly one of these two statements is true" (from the comparison with Portia
    III in the same solution).
  - "Good heavens, I can take any number of caskets that I please and put an object in one of
    them and then write any inscriptions at all on the lids; these sentences won't convey any
    information whatsoever."
  - "the suitor's error was to assume that each of the statements was either true or false."
  - "in this case one of the old Portias would have had to have made a false statement
    somewhere along the line".
  - Dagger: next test, "Portia explained that one of them contained a dagger and the other two
    were empty" (three caskets).
  The OCR of the gold and silver inscription images is missing from the text file (images);
  the wording comes from Smullyan's own solution text.
- Hemlock verse (afterword): `data/originals/the-parable-of-hemlock.md`.

## 3. Arithmetic / logic worked

First puzzle. Let F1, F2 = frog in box 1/2 (exactly one); exactly one inscription true.
- I1: XOR(F1, frog in false-inscription box). I2: (G2 and frog in false box) or (F2 and gold in true box).
- Case I1 true, I2 false: false box = 2. I1 = XOR(F1, F2) = true always. I2 = (G2 and F2) or (F2 and G1) = F2. I2 false requires F2 false: gold in 2.
- Case I1 false, I2 true: false box = 1. I1 = XOR(F1, F1) = false always. I2 = (G2 and F1) or (F2 and G2) = G2. I2 true requires gold in 2.
- Both cases: gold in box 2, frog in box 1. Jester's partial explanation (I1 true, gold in 1 makes I2 true) checked: I2's second disjunct holds.

Second puzzle, dagger in box 2 (I2 false). If I1 true: both true, contradiction. If I1 false:
exactly one true; not I1, so I2, contradiction. I1 has no consistent truth value.

## 4. Claims about other posts

- Afterword quotes the verse from "The Parable of Hemlock" (next post), described as "a related
  point", not as the Dagger's stated moral (Hemlock does not mention the Dagger).
- Manifest: order 155, first post of "A Human's Guide to Words"; posted 2008-02-01.

## 5. Not verified

- Whether the first (frog) puzzle is also Smullyan's. I searched the Portia chapters only;
  the notes say "adds the first half", which is true relative to problem 70 (the words "frog"
  and "jester" do not occur anywhere in that book's text), but I did not
  search all of Smullyan's books. If the editor wants, soften to "adds a first half, not in
  problem 70".
- The inscription images in problem 70 (OCR shows blank); wording taken from the solutions.

## 6. Judgment calls

1. Fiction: judged for what it shows (as with The Ritual). No note faults it for lacking
   evidence. The main criticism is that the explanation is left out; a fair defender may say a
   parable should leave it out. The Response says only that the king's line, read alone,
   could be taken as a verdict against logic.
2. "the credit is accurate and, if anything, modest" (Response): mild praise; the king's last
   line is close to Smullyan's solution. Could be cut.
3. Reserved words: "wrong" (the king's "wrong box" is the story's; "wrong about the boxes" on
   the jester's cry is met: the dagger is there). "false" throughout is the logical value.
4. Pronouns: the jester is "he" in the post ("as he was dragged away"); the king has no
   pronoun in the post, so I quoted the king's line instead of "he". Smullyan (historical)
   and Smullyan's suitor ("his" in Smullyan's text) keep theirs.
