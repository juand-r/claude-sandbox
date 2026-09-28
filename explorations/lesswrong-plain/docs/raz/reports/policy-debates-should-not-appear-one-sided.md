# Report: policy-debates-should-not-appear-one-sided ("Policy Debates Should Not Appear One-Sided", Yudkowsky, posted 2007-03-03)

## 1. The argument in three sentences (written before annotating)

Questions of fact should end up one-sided, because strong evidence is evidence found on one side only, but a complex policy has many consequences, so there is no reason for all its costs to fall on one side; people want one-sided policy debates because they treat arguments as soldiers. The author's own example, that some poor mother will buy a banned product and die, is a factual cost that people on both sides should admit, and denying it (by saying she deserves it) is a way of refusing to live in an unfair universe, where the birth lottery for intelligence and upbringing is not chosen. Real tough-mindedness admits the tragedy and still does the cost-benefit calculation; the author counts such deaths as tragedies and draws a moral line at capital punishment.

## 2. Sources checked (outside quotations and figures)

All fetched in this session; saved in `data/sources/raz_b2_politics/`.

**The post's footnote 1 source**: Hanson et al., "The Hanson-Hughes Debate on 'The Crack of a Future Dawn'", JET 16(1), June 2007, pp. 99-126.
URL: https://jetpress.org/v16/hanson.pdf -> `jet_hanson_hughes_2007.pdf/.txt`.
Matched: header "16(1) – June 2007"; "The Crack of a Future Dawn" (1994), if the technology to copy, or upload, human minds is developed before strong AI". `grep -i "banned|ban |store|shop|stor"` finds only "therapeutic cloning should not be banned" (l. 97), "we could ban the kinds of technologies" (l. 997) and words like "history"/"story". No banned-products stores. The journal name is also missing in the footnote ("16, no. 1"); not noted (nitpick).

**Hanson, "Paternalism Is About Bias", Overcoming Bias, 2 March 2007.**
URL: https://www.overcomingbias.com/2007/03/paternalism_is_.html (redirects to /p/paternalism_is_html) -> `ob_paternalism_is_about_bias.html`. `datePublished":"2007-03-02T10:00:00+00:00"`.
Matched: "let anything the government would have banned be sold only at special "would have banned" stores, whose customers pass a test showing they understand that regulators disapprove." Also an "Added:" line: "Many of you say paternalism is to protect the very stupid. Would you support Would-Have-Banned stores with an min IQ rule?" (not used). The author's original reply comment ("I replied") is not on the page as served (old comments not shown); not verified.

**LessWrong current text**: GraphQL `contents.html` for PeSzc9JTBxhaYRp9b saved as `lw_pd_PeSzc9JTBxhaYRp9b.html`; the only external link is the jetpress PDF, so the wrong citation is in the text LessWrong publishes now (modifiedAt 2024-02-02).

**Finucane et al. (2000)** (for the "deny all costs" note): see the Scales report. Matched: "numerous studies have shown them to be negatively related in people's minds ... the greater the perceived benefit, the lower the perceived risk" (paraphrased in the note, not quoted).

**Heritability of IQ**: Wikipedia raw wikitext, https://en.wikipedia.org/w/index.php?title=Heritability_of_IQ&action=raw -> `wiki_Heritability_of_IQ.txt` (secondary). Matched (inside a `{{Reference page|page=132|quote=...}}` template on the twin-studies sentence): "Most studies estimate that the heritability of IQ is somewhere between .4 and .8 (and generally less for children), but it really makes no sense to talk about a single value for the heritability of intelligence." Also: "most family studies estimate the heritability of IQ in the range from 0.4 to 0.8 and reviews of the literature typically summarize classical family design research with an estimate of 0.5." The quote's underlying book is not certain from the wikitext (it sits next to a Ceci 1996 citation); the note attributes it to Wikipedia only.

**Politics is the Mind-Killer** (`data/originals/politics-is-the-mind-killer.md`, posted 2007-02-18): "Politics is an extension of war by other means. Arguments are soldiers. Once you know which side you’re on, you must support all arguments of that side, and attack all arguments that appear to favor the enemy side; otherwise it’s like stabbing your soldiers in the back—providing aid and comfort to the enemy." Our note there: "Three claims, none supported".

Considered and dropped:
- "Like all primates, humans have strong negative reactions to perceived unfairness." Inequity responses are not found in every primate species tested (PubMed 36467329, Vale et al. 2022: squirrel monkeys "has not responded to inequity in previous dyadic research"; `pubmed_inequity_primates.txt`). Cut as a nitpick: the claim about humans stands, and footnote 2 names the just-world literature.
- "whether Earthly life arose by natural selection": natural selection explains the diversification of life, not its origin. Cut as a wording nitpick; read in the intended sense, the example works.
- "maybe even say it in journal articles": economists and regulators already publish values of a statistical life. Cut: the sentence is a joke, and I did not fetch a source.

## 3. Arithmetic

- Dates: Hanson post 2007-03-02; this post 2007-03-03 (`Posted:` line) = the day before. JET issue June 2007: three months after March 2007. Scales post 2007-03-13 = ten days later. Politics is the Mind-Killer 2007-02-18.
- Heritability: post's lower bound 0.6 vs summaries' 0.4: off by a third of the post's figure (0.2/0.6), above the one-fifth threshold, and "overwhelming" adds weight; hence a note.

## 4. Claims about other posts

- "Politics is the Mind-Killer" (18 February 2007): the three sentences are nearly verbatim (quoted above). Our notes there call them unsupported; my pointer agrees.
- "The Scales of Justice, the Notebook of Rationality" (13 March 2007) cites Finucane et al.; checked in its own report.

## 5. Items not verified

- The author's original reply to Hanson (presumably an Overcoming Bias comment). Would need the 2007 comment thread.
- Whether people "deny all costs" in the sense stated: I only checked the Finucane lean.

## 6. Judgment calls for the editor

- Reserved word "wrong" twice: note "The footnote cites the wrong source" and Response "a wrong citation". Evidence: the cited document postdates the post and does not contain the proposal; the right source is identified. I think it meets the word. The error is probably the book editors' (the footnote format is the book's), but it is in the text LessWrong publishes now, so I did not attribute it to anyone.
- "But even so" note (paragraph 2). The post's point is that a stated cost is not a verdict, and that stands. The note says only that the post's own reply was worded as a rebuttal. A defender could say "a cost is a point against, but I never said it decides". The note does not say the author argued for regulation. Cut it if it feels like a gotcha.
- Orphans note (libertarian paragraph). "No downside" could be read as "no downside to the buyer", but the post writes "no downside to having shops", and its own first paragraph names the orphans. I kept it as clogic, "does not follow from the post's own example", not "wrong".
- Heritability note: mixed with credit ("The post's point does not rest on the figure").
- Missing test in Hanson's proposal: one clause in the footnote note and the Response. It changes the proposal described, not the post's argument.
- Credit is given in the Response's first paragraph; I judged that leaving it out would mislead, since the thesis is sound.
