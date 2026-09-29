# Report: belief-in-the-implied-invisible

## 1. The argument in three sentences

The anti-zombie argument should not be generalized to "anything you can't see doesn't exist": a photon sent past our cosmological event horizon goes on existing although we can never again interact with it. The reason is not that the razor favours fewer objects, since its Bayesian formalizations (Solomonoff induction, Minimum Message Length) charge for the length of the laws, not the number of things they govern, and a vanishing photon would need an extra law. More precisely, we assign probability to simple, well-tested general laws and believe what they logically imply (the "implied invisible"), while a specific unseen event or law with no evidence of its own (the "additional invisible") gets no more than its prior.

## 2. Sources checked

Saved texts are in `data/sources/4b_gazp-vs-glut/` unless stated.

- Event horizon: Davis and Lineweaver, "Expanding Confusion: common misconceptions of cosmological horizons and the superluminal expansion of the universe", arXiv:astro-ph/0310808v2 (Publ. Astron. Soc. Australia 21, 2004) (`dl.txt`, lines 423-428): "Most observationally viable cosmological models have event horizons and in the ΛCDM model of Fig. 1, galaxies with redshift z ∼ 1.8 are currently crossing our event horizon. These are the most distant objects from which we will ever be able to receive information about the present day." Figure caption (line 400-401): "Our event horizon is our past light cone at the end of time, t = ∞ in this case. It asymptotically approaches χ = 0 as t → ∞." (used for the colony note: the comoving event horizon shrinks to zero).
- Occam formulation: Wikipedia "Occam's razor", raw (`wp_occam.txt`, lines 5, 23, 25): "frequently cited as Entia non sunt multiplicanda praeter necessitatem ... although Occam never used those words"; "one can cite statements such as Numquam ponenda est pluralitas sine necessitate ("Plurality must never be posited without necessity")"; "the precise words sometimes attributed to William of Ockham, Entia non sunt multiplicanda praeter necessitatem ... are absent in his extant works; this particular phrasing comes from John Punch" (citing Flew 1979 and Crombie 1959). Secondary; the note says so.
- Speed prior: Schmidhuber's page https://people.idsia.ch/~juergen/speedprior.html (`schmid_speedprior.txt`): "SPEED PRIOR A New Simplicity Measure for Near-Optimal Computable Predictions (based on the fastest way of describing objects, not the shortest) COLT 2002"; "However, M assigns high probability to certain data x that are extremely hard to compute. This does not match our intuitive notion of simplicity." Published in COLT 2002 (Lecture Notes in AI), before the post.
- Tegmark, "Parallel Universes", arXiv:astro-ph/0302131 (`data/sources/4a_explaining-vs-explaining-away/tegmark_0302131.txt`, saved by an earlier agent), line 227: "Containing unobservable entities does clearly not per se make a theory non-testable."; lines 93-96: "Such models have been popular historically, originally with the island being Earth and the celestial objects visible to the naked eye, and in the early 20th century with the island being the known part of the Milky Way Galaxy." The author cites this essay in "The Bottom Line" and "The Lens That Sees Its Flaws".
- Island-universe history: K. J. Gordon, "History of our Understanding of a Spiral Galaxy: M 33", NED Level 5 (`ned_gordon.txt`): "By the end of 1924, Hubble ( 34 ) had assembled data on 47 variables in M33 , 22 of which were Cepheids ... Applying the period-luminosity law, Hubble derived a distance of 285 kpc to M33 , and a comparable result from similar data for M31." Supports "mid-1920s". I searched for a source for Occam's razor being invoked against island universes or the stellar Milky Way and found none (WebSearch; Kragh, arXiv physics/0510111, `kragh.txt`, has no "Occam", "Ockham" or "parsimony").
- LessWrong rendering: GraphQL, `lw_3XMwPNMSbaPm2suGz.json`: "2<sup>100</sup>" twice and "2<sup>-100</sup>".

## 3. Arithmetic

- The photon crosses the event horizon in finite time. In comoving coordinates, light emitted from us at time t0 has comoving distance x(t) = c ∫_{t0}^{t} dt'/a(t') at time t. A signal sent from comoving distance x at time t reaches us iff x < χ_eh(t) = c ∫_t^∞ dt'/a(t'). Note x(t) = χ_eh(t0) − χ_eh(t). So the photon can no longer be reached from us, even by a signal at light speed, once χ_eh(t0) − χ_eh(t) ≥ χ_eh(t), i.e. χ_eh(t) ≤ χ_eh(t0)/2. With a cosmological constant χ_eh(t0) is finite and χ_eh(t) → 0 (Davis and Lineweaver, caption quoted above), so such a t exists. The post's "future time beyond which I don't expect the photon's future light cone to intercept my world-line" holds.
- Colony ship: a ship at nearly c reaches a target at comoving distance D if D < χ_eh(t0); a message sent back after arrival at time t_a reaches us only if D < χ_eh(t_a). Since χ_eh decreases, targets with χ_eh(t_a) < D < χ_eh(t0) are reachable but cannot reply. The post's scenario holds.
- MML: a 100-bit model among 2^100 models of that length gets prior about 2^-100. Correct.
- "each star made of a billion trillion decillion quarks": 10^9 x 10^12 x 10^33 (short-scale decillion) = 10^54. The Sun: 2 x 10^30 kg / 1.67 x 10^-27 kg ≈ 1.2 x 10^57 nucleons ≈ 3.6 x 10^57 quarks, so the phrase is low by a factor of a few thousand. Not noted: a rhetorical large number with no role in the argument (STANDARDS 2.4 number threshold: the reader is not misled about anything the argument uses).

## 4. Claims about other posts

- "Occam's Razor" (our notes and afterword, `annotated/afterwords/occam-s-razor.tex`): our notes there accept the descriptions of Solomonoff induction and MML and make the point about the choice of programming language in full; this post's notes point there rather than repeating it.
- "Decoherence is Simple" (`data/originals/decoherence-is-simple.md`, line 17): "What follows will be a restatement of the points in [Belief in the Implied Invisible](...), as they apply to quantum physics." Also used in "Distinct Configurations" (order 236): "The lost photon can be an implied invisible".
- The anti-zombie argument: "Zombies! Zombies?" and "The Generalized Anti-Zombie Principle" (originals read). The post is dated 2008-04-08, three days after the latter.

## 5. Items not verified

- The Milky Way / Occam story: no source found (the post says it could not find one either).
- Flew (1979) and Crombie (1959) themselves; the Punch attribution is from Wikipedia.
- Schmidhuber's COLT paper itself (I read his page, not the paper).

## 6. Judgment calls for the editor

1. The cfact on "Occam's Razor doesn't care about RAM": the post's claim is general ("Occam's Razor"), its evidence is its two named formalizations. The note says "True of the two formalizations the post names, not of every one proposed" and cites the speed prior. A fair defender might say the post meant "Occam's razor as formalized above". I kept the note because the sentence also denies the relevance of "the number of cycles it takes to compute", which is exactly what the speed prior counts. Following the Book III lesson (slips whose point survives stay out of the verdict), it is not in the In short line.
2. The cpara on "not quite right": it says the new account moves the simplicity answer onto the laws rather than replacing it. This is an analysis, supported by the post's own "It's the laws that are 'entities', costly under the laws of parsimony". I avoided saying the post contradicts itself.
3. Tegmark 2003 as prior work: "Its central point had been made before" (Response, In short). Tegmark's point is that theories with unobservable parts are testable; the "additional invisible" half of the distinction is the post's own. If this seems to overstate, change the In short to "the point about unobservables in tested theories had been made before".
4. The Occam misattribution cfact: a factual slip in a sentence stated as fact ("That was Occam's original formulation") whose point survives; it is in the notes and the Response, not in the In short line.
5. The scope sentence in the Response ("The post does not return to its opening case ...") is scope only, one sentence.
6. Reserved words: "wrong" only in paraphrase of the post's own "would have consistently turned out to be wrong". No "My reading".
