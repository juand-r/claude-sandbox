# Report: do-we-believe-everything-we-re-told

## 1. The argument in three sentences

Descartes held that we understand a proposition first and then accept or reject it;
Spinoza held that understanding includes accepting, and rejecting takes a further step.
Daniel Gilbert tested this: interrupting people made them misremember statements labeled
false as true but not the reverse, and people doing a digit-search task let crime-report
statements labeled false change the prison terms they recommended. So we should be careful
about unreliable information, especially when distracted.

## 2. Sources checked

All saved in `data/sources/raz_b2b_fresh/`.

- Gilbert, Krull and Malone (1990), JPSP 59: 601-613, from Gilbert's Harvard page
  https://dtg.sites.fas.harvard.edu/Gilbert%20et%20al%20(UNBELIEVING).pdf (`gkm1990.pdf/.txt`).
  Matched: "interruption had no effect on the correct identification of true propositions
  (55% when uninterrupted vs. 58% when interrupted), but did significantly reduce correct
  identification of false propositions (55% when uninterrupted vs. 35% when interrupted)";
  "Thirty-five female students"; "On 4 of these 12 trials a 500Hz tone sounded ... Of these 4
  interrupted critical trials, 2 were followed by the signal word true and 2 by the signal
  word false"; interaction "F (1, 32) = 5.30, p = .028". Spinoza: "all ideas are accepted
  (i.e., represented in the mind as true) prior to a rational analysis of their veracity".
  Philosophers: "In the centuries that followed, many psychologists (e.g., Bain, 1859; James,
  1890) and philosophers (e.g., Reid, 1764/1895; Russell, 1921) found cause to question the
  Cartesian distinction ... Nonetheless, modern psychology continues to embrace the twin
  Cartesian notions". Prediction: "interruption should cause Spinozan systems to mistake false
  ideas for true ones, but not vice versa." Background: "What is so interesting about these
  instances of inappropriate belief is that, in general, each is exacerbated by cognitive load
  and interruption", in a section naming "attribution, persuasion, and lie detection".
- Gilbert, Tafarodi and Malone (1993), JPSP 65: 221-233, from
  https://dtg.sites.fas.harvard.edu/Gilbert%20et%20al%20(EVERYTHING%20YOU%20READ).pdf
  (`gtm1993.pdf/.txt`; Table 1 is an image, `gtm_imgs/img-000.jpg`, which I viewed).
  Table 1: uninterrupted 6.03 / 7.03 years, interrupted 5.83 / 11.15. Text: "Seventy-one
  female students"; "Three subjects were omitted ... Of the remaining 68 subjects, 34";
  "statements printed in black were true statements, but that statements printed in red were
  false"; "recommend a prison term between 0 and 20 years"; "the prison terms recommended by
  uninterrupted subjects were only marginally affected by the nature of the false statements
  they had read, F (1, 66) = 3.42, p < .07, but ... interrupted subjects were reliably
  affected ... F (1, 66) = 97.03, p < .001".
- Robin Hanson, "Policy Tug-O-War", https://www.overcomingbias.com/p/policy_tugowarhtml
  (`hanson_tugowar.html/.txt`): about policy dimensions and "pull policy ropes sideways"; no
  mention of Descartes, Spinoza or philosophers (searched the extracted body text).
- Hasson, Simmons and Todorov (2005), Psychological Science 16: 566-571, PubMed abstract
  (`pubmed_16008791.txt`): "interrupting the encoding of a statement's veracity decreased
  memory for the statement's falsity when the false version of the statement was
  uninformative, but not when the false version was informative"; "The findings suggest that
  comprehending a statement may not require believing it". Full text not read.
- Nadarevic and Erdfelder (2013), Memory & Cognition 41: 176-186, PubMed abstract
  (`pubmed_22972664.txt`): "The results of both experiments clearly contradict the Spinozan
  model but can be explained in terms of the Cartesian model."
- Also read, not cited in notes: Richter, Schroeder and Wohrmann (2009), JPSP 96: 538-558
  (`richter2009.pdf/.txt`, from gwern.net): "individuals are able to reject false assertions
  efficiently when they have validity-relevant beliefs."

## 3. Arithmetic

- 11.15 / 5.83 = 1.91 ("nearly twofold"; note says 1.9).
- Hasson et al. July 2005; post October 2007: about two years.

## 4. Claims about other posts

- "Your Strength as a Rationalist" (order 27): our note there already cites Hasson et al.
  (2005) against Gilbert (1993). Per STANDARDS 2.5 the first occurrence is there; here I gave
  a fuller note because this post describes the experiments, with "see also the note on
  'Your Strength as a Rationalist'". The editor may prefer to shorten one of the two.

## 5. Not verified

- Gilbert (1991), "How Mental Systems Believe" (`g1991.pdf`) is a scan without text; not used.
- Full texts of Hasson et al. and Nadarevic and Erdfelder: abstracts only.
- The post's opening history (early anchoring experiments under load leading Gilbert to the
  question) is not contradicted by anything I read; the note only adds the 1990 paper's own
  account of the wider evidence.

## 6. Judgment calls

- "sits uneasily with the post's own source" for "philosophers pretty much went along with
  Descartes": the post's sentence is casual ("pretty much"), and GKM's list of dissenting
  philosophers (Reid, Russell) is short. I did not write "contradicts".
- The \cfact on the Hanson footnote: it may be a placement slip in the book edition. The note
  states only what the cited post contains.
- The skeleton made by `new_post.py` failed the verbatim check: the post's in-text marker for
  the 1993 paper is printed "2" and links to "#footnote2", so the converter left the third
  footnote as a stray paragraph. I replaced `\href{\#footnote2}{2}` with
  `\cauthor{<footnote 3 text>}` and removed the stray paragraph. The checker then prints OK
  (670 words). No word of the post changed; the printed marker "2" (a slip in the original,
  since the footnote is numbered 3) is not reproduced. The editor may want `md2tex.py` fixed.
- The \clogic "The results fit Spinoza's model, but the model was already disputed": the
  fair-defender reply "I only reported the study" is answered by the post's own "bear out".
