# Report: evaluability-and-cheap-holiday-shopping ("Evaluability (And Cheap Holiday Shopping)", Yudkowsky, posted 2007-11-28)

## 1. The argument in three sentences (written before annotating)

Hsee's studies show that an attribute that is hard to judge on its own (a dictionary's 20,000
entries, 8 oz of ice cream) carries little weight when an option is seen alone and a great
deal when two options are seen side by side, so preferences reverse between separate and
joint evaluation; Slovic's gambles show the same thing, since adding a 5-cent loss makes a
$9 win evaluable and the gamble more attractive. The torn cover or the overfilled cup has a
clear good or bad feeling attached, while bare numbers do not. The joke application: a
gift-giver who wants to look generous should buy an expensive item from a cheap category,
because the recipient sees the gift alone.

## 2. Sources checked

Local copies in `data/sources/raz_b2b_eval/`.

1. Hsee (1996), OBHDP 67: `hsee1996.pdf/.txt`, from https://pages.ucsd.edu/~cmckenzie/Hsee1996OBHDP.pdf
   - Figure 1 read from the rendered page (`h96p-02.png`): joint A 19 (n 39), B 27 (n 39);
     separate A 24 (n 39), B 20 (n 38). Matches the post.
   - "Respondents were 116 unpaid college students"; "asked to assume that they were a music
     major ... planned to spend between $10 and $50".
   - "in separate evaluation WTP values were higher for Dictionary A than for Dictionary B
     (t = 1.69, p = .1). The PR was highly significant (t = 4.56, p < .001)"; joint: t = 7.11,
     p < .001.
2. Hsee (1998), JBDM 11: primary text not reachable (Wiley paywall; the Chicago Booth PDF link
   in Wikipedia returns 404). Details taken from:
   - Vonasch et al. (2023), Collabra: Psychology 9(1), preprint v7 from OSF
     (https://osf.io/download/rzwpj/, project https://osf.io/9uwns/): `vonasch2023.pdf/.txt`.
     Gift vignettes quoted: "The worst costs $5 and the best costs $50. The one your friend
     bought you costs $45." / "The worst costs $50 and the best costs $500. The one your friend
     bought you costs $55." "The original study only included the coat and scarf conditions,
     not the joint condition". Joint result: "participants in the joint condition preferred the
     scarf (63%) to the coat (37%; binomial: p = .002)". Interpretation: "People may think the
     cheapest coat is such low quality that it is not particularly worth having ... If this
     latter interpretation is correct, that would undermine the validity of this paradigm ...
     because it would mean this paradigm does not produce a reversal"; "we were unable to test
     which interpretation is correct".
     Ice cream original figures in the supplement: "Condition 1 (Separate_Vendor H): N=23,
     M=$1.66 / Condition 2 (Separate_Vendor L): N=23, M=$2.26"; "Condition 1 (Vendor H): N=23,
     M=$1.85 / Condition 2 (Vendor L): N=23, M=$1.56"; "number of participants in each
     condition was not stated in the original article, it was assumed". Vendor H = "10 oz cup
     and puts 8 oz", Vendor L = "5 oz cup and puts 7 oz". Replication: less-is-better for ice
     cream d = 0.32 (original 0.74), and not significant if two outliers are kept.
   - Wikipedia "Less-is-better effect" (raw wikitext, `wiki_less_is_better.txt`), quoting Hsee:
     "if gift givers want their gift recipients to perceive them as generous, it is better for
     them to give a high-value item from a low-value product category (e.g. a $45 scarf) rather
     than a low-value item from a high-value product category (e.g. a $55 coat)." (Basis for
     "Hsee's own conclusion".)
3. Slovic, Finucane, Peters, MacGregor, "Rational actors or rational fools" (2002), J. Socio-
   Economics 31: `slovic2002.pdf/.txt`, from
   https://cpb-us-w2.wpmucdn.com/u.osu.edu/dist/e/65099/files/2018/08/2002_Slovic_Finucane_etal._Rational_actors_or_rational_fools-2ltdwze.pdf
   - Gives only "The mean response to the first gamble was 9.4. When a loss of 5/c was added,
     the mean attractiveness jumped to 14.9". Defect "is an affective variable that translates
     easily into a precise good/bad response".
4. Slovic, Finucane, Peters, MacGregor, "The affect heuristic" (2002 chapter; reprinted EJOR 177,
   2007): `slovic_affect_heuristic_2002.pdf/.txt`, from
   https://bear.warrington.ufl.edu/brenner/mar7588/Papers/slovic-affect-heuristic-2002.pdf
   - Table: "29/36 to win $2  $1.25  13.2 / 7/36 to win $9  $2.11  7.5".
   - "Subjects were told that a pair of bets would be selected and the bet that received the
     higher attractiveness rating (or the higher price, or that was preferred in the choice
     task) would be the bet they would play ... Some of the gambles were, in fact, actually
     played." (No "randomly"; not worth a note.)
   - "The results exceeded our expectations." 9.4 / 14.9; 25-cent loss "mean = 11.7".
   - "asking 96 University of Oregon students ... Whereas only 33.3% chose the $9 gamble over
     the $2, 60.8% chose the ($9; 5¢) gamble over the $2."
   - No condition with both gambles side by side is reported.

## 3. Arithmetic

- EV of 7/36 to win $9: 7 x 9 / 36 = 63/36 = 1.75. With 29/36 lose $0.05: 1.75 - 1.45/36 =
  1.75 - 0.0403 = 1.7097, "about 1.71". Both below the sure $2.
- EV of 29/36 to win $2: 58/36 = 1.61 (not used in a note).
- Group sizes for 33.3% / 60.8% of 96: 15/45 = 33.3%, 31/51 = 60.8% (45 + 51 = 96), so "half"
  is approximate. Not used in a note.
- Scarf replication: 22/41 etc. not applicable; 63% = 85/134 (85 + 49 = 134).

## 4. Claims about other posts

- None beyond the citation to Slovic et al. The previous post, "The Affect Heuristic"
  (2007-11-27), gives the full citation for "Rational Actors or Rational Fools". I have not seen
  final notes for that post (another agent, same batch). If its notes discuss the Slovic papers,
  the footnote note here should agree with them.

## 5. Not verified

- Hsee (1998) primary text: gift and ice cream details come from the 2023 replication and
  Wikipedia (both quote or reproduce the original materials).
- Price claims in the shopping paragraph: the Wii's US list price was $249.99 from launch
  (November 2006) until September 2009 (Wikipedia "Wii", raw wikitext, `wiki_wii.txt`: "priced
  at {{USD|249.99|2006}}", "dropping the MSRP from {{USD|249.99}} to {{USD|199.99}}"). So "$400
  on a Nintendo Wii" is not the list price (off by 60%). The iPod Touch price was not checked.
  No note: the paragraph is a joke, and the point (the top of one class against the bottom of
  another at equal spending) does not depend on the exact prices. The editor may disagree.
- Japanese $50 melons: not checked; part of the joke.
- Footnote 1 names the journal "Behavioral Decision Making" (it is the Journal of Behavioral
  Decision Making). Not noted (nitpick).

## 6. Judgment calls

1. The clogic on "special case": relies on the 2023 replication (post-dates the post) and on the
   replicators' hedged interpretation. The note keeps their hedge ("may mean", "could not
   settle"). The Response says the gift study is "the weakest example"; it does not say the
   gift effect is not real (it replicated strongly in separate evaluation).
2. The dictionary note (p = .1) is a description of significance, not an error by the post. I
   kept it because the post's explanation leans on the separate-evaluation preference.
3. "Of course, it only works if ..." is called a prediction, not a finding. A fair defender could
   say "Of course" marks an inference. The note calls it "reasonable".
4. The footnote-3 note (most gamble figures are in "The Affect Heuristic", not "Rational
   Actors") is a citation point; I kept it in the margin for readers who check, and removed it
   from the Response as minor.
5. The EV arithmetic in the follow-up-experiment note is added context that makes the post's
   point stronger, not a criticism.
6. No reserved words used.
