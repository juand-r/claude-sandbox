# Report: Bayesians vs. Barbarians (batch 6c, order 334)

## 1. The argument in three sentences (written before annotating)

The post rejects the view that a society of rationalists must lose a war to fanatics because each rational citizen would rather someone else fight. In principle, it says, agents with the author's decision theory (the one behind one-boxing on Newcomb's problem) coordinate at Pareto optima, for example by agreeing in advance to a lottery that picks soldiers who then fight; in practice, human rationalists can rely on caring for others, a culture that does not teach defection, and, failing that, incentive mechanisms such as courage drugs and shooting deserters, agreed on before the lottery, and they must obey unified orders because an uncoordinated mob gets slaughtered. The point, the author says, is self-image: a reader should believe that a society of people like them could fight and win, though how exactly remains an open question.

## 2. Sources checked

All saved in `data/sources/batch06c_bayesians-vs-barbarians/` (plus `insert_notes.py`, the script that inserted the notes).

| Claim in our notes | Source | Exact words matched |
|---|---|---|
| Vegetius maxim | thelatinlibrary.com/vegetius3.html (`vegetius3.html`), preface to book 3 | "Igitur qui desiderat pacem, praeparet bellum; qui uictoriam cupit..." |
| Vegetius date | Wikipedia "Vegetius" raw (`wiki_Vegetius.txt`) | "The latest event alluded to ... is the death of the Emperor Gratian (383); the earliest attestation ... in 450" |
| Olson quotation | secondary: arXiv 1906.09874 (`arxiv_1906.09874.txt`), and econport.gsu.edu (`econport_solutions.html`) | arXiv: "unless the number of individuals in a group is quite small, or unless there is coercion or some other special device to make individuals act in their common interest, rational, self-interested individuals will not act to achieve their common or group interests." Econport has "their common group interests" (no "or"). I used the arXiv wording and said in the note that the book was not opened. |
| Paradox of voting; causal theories | SEP "Voting" (Jason Brennan), https://plato.stanford.edu/entries/voting/ (`sep_voting.txt`) | "This leads to the “paradox of voting”(Downs 1957): Since the expected costs (including opportunity costs) of voting appear to exceed the expected benefits"; "(Tuck 2008; Goldman 1999) ... These causal theories of voting claim that voting is rational provided the voter sufficiently cares about being a cause or among the joint causes of the outcome." |
| Program equilibrium, prior work | Wikipedia "Program equilibrium" raw (`wiki_program_equilibrium.txt`) | "The term was introduced by Moshe Tennenholtz in 2004. The same setting had previously been studied by R. Preston McAfee, J. V. Howard and Ariel Rubinstein"; "Multiple authors have independently proposed the following program ... (Tennenholtz2004, Howard1988, McAfee1984)": cooperate iff opponent_program == this_program; "(CliqueBot,CliqueBot) is an equilibrium" |
| 2014 paper | arXiv 1401.5577 abstract (`arxiv_1401.5577.html`); authors Barasz, Christiano, Fallenstein, Herreshoff, LaVictoire, Yudkowsky; date 2014/01/22 | "cooperation does not require exact equality of the agents' source code" |
| Other side of the dispute | SEP "Prisoner's Dilemma" (Steven Kuhn), section 7 (`sep_pd.txt`) | "One controversial argument that it is rational to cooperate in a PD relies on the observation that my partner in crime is likely to think and act very much like I do. (See ... Binmore 1994, chapters 3.4 and 3.5, for a reformulation and extended rebuttal.)"; "The counter argument, of course, is that my action is causally independent of my replica’s. Since I can’t affect what my accomplice does and since, whatever he does, my payoff is greater if I defect, I should defect." |
| Britain's volunteers, conscription 1916 | Wikipedia "Kitchener's Army" raw; "Military Service Act 1916" raw | "By 12 September, almost half a million men had enlisted." "By the beginning of 1916, enthusiasm for volunteering had waned." Act "passed by the Parliament of the United Kingdom", "royal_assent = 27 January 1916" |
| Hobbes | Leviathan, ch. 21, Project Gutenberg #3207 (`leviathan_gutenberg.txt`); also Bennett's modernized version (`hobbes_part2_bennett.pdf/.txt`) | "a man that is commanded as a Souldier ... may neverthelesse in many cases refuse, without Injustice ... they are not esteemed to do it unjustly, but dishonourably ... But he that inrowleth himselfe a Souldier, or taketh imprest mony ... is obliged, not onely to go to the battell, but also not to run from it, without his Captaines leave. And when the Defence of the Common-wealth, requireth at once the help of all that are able to bear Arms, every one is obliged" |
| British WWI executions | Wikipedia "Shot at Dawn Memorial" raw | "It commemorates the 309 British Army and Commonwealth soldiers executed after courts-martial for desertion and other capital offences during World War I." |
| Order No. 227 | Wikipedia "Order No. 227" raw | "issued on 28 July 1942"; "put them directly behind unstable divisions and require them in case of panic ... to shoot in place panic-mongers and cowards" |
| Vietnam draft lottery | Wikipedia "Vietnam War draft" raw (the "Draft lottery (1969)" title redirects there) | "the process ... was biased against the poor and the uneducated. The government decided in 1969 to reduce this bias by introducing a random element ... A lottery based on birth dates was conducted by the Selective Service System on December 1, 1969" |
| Swiss referendum | Wikipedia "2013 Swiss referendums" raw | "Three federal referendums were held on 22 September 2013"; "Abolition of compulsory military service ... 644,985 | 26.8 | 1,762,811 | 73.2 ... Rejected" |
| Fragging | Wikipedia "Fragging" raw | "According to author George Lepre, the total number of known and suspected fragging cases using explosives in Vietnam from 1969 to 1972 totalled 904, with 99 deaths ... Most of the victims or intended victims were officers or non-commissioned officers." |

## 3. Arithmetic recomputed

- Election margins. 100,000 to 99,998: remove any one winning vote, 99,999 to 99,998, still a win; so no single voter is pivotal. 100,000 to 99,999: remove any one winning vote, 99,999 to 99,999, a tie; so each winning voter is pivotal. The post's two sentences are consistent with this.
- The long sentence in the self-image paragraph: counted by script from "And it's a different sort of self-image" to "waiting for them.": 178 words; "because" 6 times, "and because" 5 times.
- Swiss vote: 1,762,811 / (644,985 + 1,762,811) = 73.2 per cent. Checked.

## 4. Claims about other posts

- "Previously" quote: data/originals/why-our-kind-can-t-cooperate.md lines 95 to 99, matched word for word (posted 2009-03-20).
- "Evil" link: are-your-enemies-innately-evil.md (2007-06-26): "We see far too direct a correspondence between others’ actions and their inherent dispositions"; "If it took a mutant to do monstrous things, the history of the human species would look very different."
- Marching link: your-price-for-joining.md (2009-03-26): "It seems to me that people in the atheist/libertarian/technophile/sf-fan/etcetera cluster often set their joining prices *way way way* too high."
- Newcomb pointer: our notes on newcomb-s-problem-and-regret-of-rationality (TDT 2010, FDT 2017; the dispute and Lewis's "standoff"). The Newcomb original says causal decision theorists accept precommitment (line 44); I did not rely on that here, because in the lottery case one AI's precommitment does not cause the outcome, so the analogy would mislead.
- True PD pointer: our notes on the-true-prisoner-s-dilemma (dominance checked; Fischbacher et al. on conditional cooperators).
- Utility functions need not be solipsistic: agrees with our note on why-our-kind-can-t-cooperate ("Decision theory takes what an agent values as given"); I did not add a note.
- beisutsukai: pointer to The Ritual and Final Words, following review_log (whole-book pass will move the gloss to The Ritual).
- Dates from the manifest: Reversed Stupidity 2007-12-12; Fictional Evidence 2007-10-16.

## 5. Not verified

- Olson's sentence was not checked in the book itself (archive.org copy is lending-only). Two secondary sources differ by one word ("common or group" against "common group").
- McAfee 1984 and Howard 1988 were not opened; they are cited as Wikipedia reports them.
- Binmore 1994, Downs 1957, Goldman 1999, Tuck 2008 are cited as the SEP entries report them.
- The post's remark on the US military's concern for casualties was not checked; the note calls it an aside without evidence.
- web.archive.org was not needed. Gutenberg reset the connection twice before the third request succeeded.

## 6. Judgment calls for the editor

1. Reserved word: "never" appears only in "people who never agreed" (fragging note), a plain description, not a charge.
2. The lottery note says the lottery "does not by itself remove the temptation to free ride": each AI taken alone could do better by leaving its code unchanged. This is my reasoning from the post's own sausage premise, not from a source. I think it is a reading aid rather than a charge, since the post itself turns to enforcement for humans ("if 'be reflectively consistent ...' is not sufficient motivation"). Cut it if the editor judges it an unsourced objection.
3. "These are the ordinary routes to cooperation in game theory and economics" (reputation, social preferences, incentives) is stated without a citation as a commonplace.
4. The fragging note. The sentence is the most striking in the post. I kept it narrow: the sentence is consistent as an argument from prior agreement; the post does not say whether the killing was right on other grounds; plus Lepre's figures. I removed this point from the Response to avoid giving it weight there. The editor may think the "does not say" sentence is still a scope complaint worth cutting.
5. The drafts note: "The claim that current drafts are not 'collective attempts by a populace' is given without evidence." The post's sentence is general, so I treated it as a claim, while calling "tool of kings" a figure of speech. The Swiss 2013 vote is after the post and is kept as information in the notes only, not in the Response or the honest section.
6. The executions note originally said real armies used the measure "without a prior agreement"; I removed that because many executed British soldiers were volunteers who had enlisted (Hobbes's "inrowleth" case). The notes now say only that the measure was used, and that what the post adds is agreement by everyone before the lottery.
7. Response: "The practical case is better supported." The post's first human remedy (a culture that believes deserting "is the same as deciding for the Barbarians to win") still rests on its Newcomb position; only the fallback does not. The Response says "the post's fallback is the remedy Olson named", so I think it stays within that line.
8. Summary is 200 words, above the model's 150, for a 2,279-word post. Honest section is 501 words.
9. Skeleton repair: md2tex put the opening blockquote into the "Previously:" line with literal ">" markers. I split it into the link line and a quote environment (markup only; verbatim check OK). The tooling issue may affect other posts that open with a link followed by a blockquote.
