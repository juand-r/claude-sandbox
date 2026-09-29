# Report: One Life Against the World (batch 5c, order 287)

## 1. The argument in three sentences

The post grants that saving one life probably feels as good as saving the world (the
author's own anonymous blog comment felt like a scientific insight), and quotes the Mishnah's
"Whoever saves a single life, it is as if he had saved the whole world" as a beautiful thought
that produces a warm glow. It then argues that beyond the feeling there is a gigantic
difference: it names three reasons one might deny that saving more lives is proportionally
better (a qualitative duty, Greek virtue, the unimaginable value of one life), answers the third
with "two human lives are twice as unimaginably valuable" and the railroad case, and applies
this to a philanthropist choosing between a cure for 100 people and one for 10,000.
It concludes that when lives are at stake there is a duty to maximize, as strong as the duty to
save lives, and that whoever knowingly saves one life when they could have saved two has
"damned themselves as thoroughly as any murderer."

## 2. Sources checked

Saved in `data/sources/5c_one-life-against-the-world/` unless stated.

- Mishnah Sanhedrin 4:5, Sefaria API (`mishnah_4_5.json`, all eleven versions in
  `mishnah_4_5_versions.txt`).
  - Vilna/Torat Emet Hebrew: "וְכָל הַמְקַיֵּם נֶפֶשׁ אַחַת מִיִּשְׂרָאֵל, מַעֲלֶה עָלָיו הַכָּתוּב כְּאִלּוּ קִיֵּם עוֹלָם מָלֵא" ("one soul from Israel").
  - Kaufmann manuscript (Be'eri): "וְכָל הַמְקַיֵּם נֶפֶשׁ אַחַת, מַעֲלִין עָלָיו כְּאִלּוּ קִיֵּם עוֹלָם מָלֵא" (no "from Israel").
  - Kulp translation (Mishnah Yomit): "the witness is answerable for the blood of him [that is
    wrongfully condemned] and the blood of his descendants [that should have been born to him] to
    the end of the world." Note quotes the part from "the blood of his descendants".
  - German edition (Mischnajot, Berlin 1887-1933), note 43: "Jerusch., Handschriften und and.
    Zeugnisse lesen nicht: מישראל. Es hat auch keinen rechten Sinn, da doch der erste Mensch kein
    Israelit war." The note paraphrases this.
- Jerusalem Talmud Sanhedrin 4:9 (Guggenheimer), `Jerusalem_Talmud_Sanhedrin.4.9.json`:
  "וְכָל הַמְקַיֵים נֶפֶשׁ אַחַת מַעֲלִין עָלָיו כְּאִילּוּ קִיֵים עוֹלָם מָלֵא" (no "from Israel");
  English "for anybody who preserves a single life it is counted as if he preserved an entire world".
- Babylonian Talmud Sanhedrin 37a (William Davidson), `Sanhedrin.37a.json`: "וְכׇל הַמְקַיֵּים
  נֶפֶשׁ אַחַת מִיִּשְׂרָאֵל". Confirms the printed Bavli reads "from Israel".
- John Taurek, "Should the Numbers Count?", Philosophy & Public Affairs 6(4), 1977, scan at
  https://sites.pitt.edu/~mthompso/readings/taurek.pdf (`taurek.pdf`; image-only, so p. 303 read
  by eye and transcribed in `taurek_p303_transcribed.txt`). Matched: "I feel compelled to deny
  that any third party, relevant special obligations apart, would be morally required to save
  the five persons and let David die." and "Why not give each person an equal chance to survive?
  Perhaps I could flip a coin."
- Stanford Encyclopedia, "Contractualism", https://plato.stanford.edu/entries/contractualism/
  (`sep_contractualism.txt`): "Consider the following situation, drawn from a famous article by
  John Taurek (Taurek 1977)." and "Many contractualists, however, wish to capture the intuition
  that you ought to save the five."
- Stanford Encyclopedia, "Doing vs. Allowing Harm", https://plato.stanford.edu/entries/doing-allowing/
  (`sep_doing-allowing.txt`): "consequentialists believe that doing harm is no worse than merely
  allowing harm while anti-consequentialists, almost universally, disagree." The note quotes
  "while anti-consequentialists, almost universally, disagree." and paraphrases the first half.
- Nick Bostrom, "Astronomical Waste" (Utilitas 2003), https://nickbostrom.com/papers/astronomical-waste/
  (`bostrom_aw.txt`): "that the potential for approximately 10 38 human lives is lost every
  century that colonization of our local supercluster is delayed" (superscript lost in extraction).
- Robin Hanson, "RAND Health Insurance Experiment", Overcoming Bias, 8 May 2007, the post's first
  addendum link (now https://www.overcomingbias.com/p/rand_health_inshtml; `ob_rand.txt`):
  "thousands of people randomly given free medicine in the late 1970s consumed 30-40% more
  medical services ... but were not noticeably healthier !"
- The post's second addendum link (spiegel.de/international/spiegel/0,1518,363663,00.html)
  returned 403. Identified through David Wiley's 2007 post, which links that exact URL as "a
  fascinating interview on Spiegel with James Shikwati" (`opencontent.html`), and a web search
  giving the title "For God's Sake, Please Stop the Aid!". The interview text itself was not read;
  the note describes it only as Shikwati arguing that aid does more harm than good, which is
  how Wikipedia summarizes his view.
- Wikipedia, "James Shikwati" (raw, `shikwati_wiki.txt`): "calls Shikwati’s criticisms of foreign
  assistance “shockingly misguided”". Cited as Wikipedia.

## 3. Arithmetic

- Philanthropist: 10% of 100,000 = 10,000 deaths, against 100; factor 100 (script
  `data/sources/5c_the-allais-paradox/check_allais.py`, last lines of its output).
- "six billion": world population in May 2007 was about 6.6 billion; within a tenth, and a
  round figure, so no note.
- Bostrom's 10^38 is his figure; not recomputed.

## 4. Claims about other posts

- Scope Insensitivity (`data/originals/scope-insensitivity.md`): "An alternative hypothesis is
  “purchase of moral satisfaction.” People spend enough money to create a *warm glow* in
  themselves". Our notes there: "Every study in the post asks people to state what they would
  pay, or to judge proposed programs; none observes real giving." My pointer paraphrases this.
- No other post is characterized.

## 5. Not verified

- The Spiegel interview text (403). Only its identity and topic are used.
- The RAND study itself (Brook et al. 1983); used only as described in Hanson's post.
- Stuart Armstrong's comment was not looked up; the post reports it and the notes only restate it.
- Whether Taurek's view is correctly called "the first view" of the post (a "qualitative duty to
  save what lives you can") is my reading: Taurek denies a duty to save the greater number and
  proposes a coin toss, which fits "just fulfilling the same duty". I describe him as a defender of
  that view, not as the post's target.

## 6. Judgment calls for the editor

- Reserved words: "false witness" (a legal term in the Mishnah context), fine. No other reserved
  word in my text. The railroad note says the rescuer "cannot be right", paraphrasing the post's
  own verdict.
- The railroad-case note says the first two views "also condemn the rescuer, since the second
  child can be saved at no cost to the first". This is my reading of the post's own descriptions
  of those views (a duty to save "what lives you can"; virtue). The same point is the core of the
  Response and of the "In short" line ("argued from a case with no trade-off and applied to a
  case with one"). Please check it passes the fair-defender test: the author could say the case
  also targets the "points"/credit framing; I grant that the case works against the third view.
- The murder note: the post's "knowingly" is kept; I call the claim "given without argument". The
  post's only support is the railroad case and "I don't think it is different".
- Addendum note: calls the Shikwati view "one side of a contested debate" with Sachs via
  Wikipedia. Could be judged a nitpick of a side remark; I kept it because the post states
  "counterproductive" without a hedge and the only support is an interview.
- Bostrom credit note: optional; kept as prior work supporting the post.
- Pronouns: "his descendants ... born to him" are inside a quotation of the Mishnah translation;
  "he" in the Talmud line is the post's quotation.
