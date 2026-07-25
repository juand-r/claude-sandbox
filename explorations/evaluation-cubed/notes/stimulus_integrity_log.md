# Stimulus-integrity log

Protocol from arXiv:2607.13707 ("The Test Oracle Problem in Synthetic LLM-as-Judge
Corpora"), which argues that aggregate statistics cannot distinguish a fabricated effect
("disappearance") from a real effect whose magnitude or direction has been bent
("distortion"), and that the only reliable guard is inspecting raw stimuli *before*
computing any statistic. Their recommended checks, run here, in order.

## Round 1 (2026-07-25, initial build)

**1. Mechanical no-op check.** 0/510 corrupted claims were string-identical to their true
counterpart, under both exact and whitespace-normalised comparison. This is the cheap
oracle their positive control demonstrates: our corruption step is a claim substitution,
so it is fully string-checkable at zero API cost.

**2. Word count per condition.** plain 77 / polished 130 / padded 286. Flat across
quality levels within each style (max deviation 2%), so the corruption step does not
interact with length. Good.

**3. Degeneration rates.** No fragments (<3 words) anywhere. But: **61–68 of 85 `plain`
answers were verbatim, whitespace-normalised concatenations of the statement list.**

**FAULT FOUND.** The `plain` renderer instruction ("4–7 short sentences, no formatting")
was satisfiable by emitting the six claims one per sentence with at most a pronoun
substitution. So the `plain` condition was not a rewrite at all; it was the raw stimulus.

Why this matters, concretely: the study's central quantity is the judge's sensitivity to
quality-preserving *restyling*. If one of the three styles is un-restyled raw material and
reads as a bare fact list, the measured style effect is partly an artefact of comparing
"list" against "prose", which would **inflate** the headline bias estimate. This is
precisely the distortion mode 2607.13707 describes: a real effect whose magnitude is bent
by a stimulus fault, invisible in aggregate statistics.

**Fix.** The `plain` instruction now forbids one-statement-per-sentence restatement and
requires combining related statements, varying sentence structure, and joining with
connectives. Re-rendered all 425 `plain` answers.

## Round 2 (after fix)

**1. No-op check.** 0/510. Unchanged.

**2. Word count.** plain 99 / polished 130 / padded 286. `plain` rose from 77 to 99 words,
consistent with genuine synthesis rather than concatenation. Still flat across k.

**3. Degeneration.** 0 fragments, **0 verbatim copies** in all 15 conditions.

**4. Claim fidelity.** 7621/7650 = 99.6% of claim slots assert the intended version.
Verified true-claim counts per level: 6.00 / 5.02 / 4.01 / 3.01 / 1.99 against intended
6 / 5 / 4 / 3 / 2. The construction does what it says.

**5. Rendering-level no-ops.** 5/1020 answers at k>0 where the checker detected no false
claim. 0.5%; reported, not swept up.

## Manual reading (the check that actually found things)

Read 20+ raw items spanning all three styles and quality levels 0–4.

- `plain` post-fix: genuine synthesis. Claims are merged into single sentences, reordered,
  and connected ("…, which allows two parties to agree on a secret without previously
  sharing one"). No longer list-shaped.
- `polished`: framing sentence, bulleted body with bolded key terms, closing sentence.
- `padded`: hedged and repetitive, roughly double length, same claims.
- Corruptions are minimal and plausible in every item read: 120→140 feet, North→South
  Carolina, wing-warping→ailerons, Orville/Wilbur role reversal.

One apparent error on first reading turned out to be my own: in it0072 I flagged the
12-horsepower engine claim as suspicious, since ~12 hp is historically correct. Checking
the pair showed the horsepower is held constant across both versions and the corruption is
the *builder* (Charlie Taylor → "the Wright brothers"). A minimal entity substitution,
correctly constructed. Worth recording because it is exactly the kind of thing that looks
like a data fault from an aggregate view and is resolved in ten seconds by reading the
raw pair — which is 2607.13707's whole argument.

**Verdict: stimuli are sound as of round 2.** All statistics in the paper are computed on
the round-2 corpus.
