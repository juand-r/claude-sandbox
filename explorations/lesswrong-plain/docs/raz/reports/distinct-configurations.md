# Report: distinct-configurations

## 1. The argument in three sentences

Placing a "sensitive thingy" S on one arm of the Mach–Zehnder setup of "Configurations and
Amplitude" adds S's state to every configuration, so the two amplitude flows that used to
cancel at Detector 1 now go to distinct configurations (S in No, S in Yes) and the photon
reaches each detector a quarter plus a quarter of the time. This holds whether or not anyone
reads S, knows S exists, or could ever learn its state, so distinctness of configurations is
a physical fact with experimental consequences and not a state of belief (with the caveat
that S's nudge must exceed its original spread). Early physicists, seeing interference vanish
when a sensor was added, concluded that knowledge or conscious observation mattered; the post
argues that clues available even then (unread sensors, stray particles) showed otherwise, and
that the "Common Wisdom" of epistemic possibilities and conscious collapse persisted even
after the theory predicted that any nudged particle would do.

## 2. Sources checked

All saved in `data/sources/4c_joint-configurations/`.

- Figures 1 to 4 of the post, fetched as PNG renderings from Cloudinary (`dc_fig1.png`,
  `dc_fig2.png`, `dc_fig3.png`, `dc_fig4.png`). Viewed. Figure 1: the interferometer with a
  green dot labelled "Sensitive Thingy S" on the A–C path; the D–E path is drawn dashed.
  Figure 3: a red block between B and D. Figure 4: same as Figure 1 (dashed D–E line too).
  "Configurations and Amplitude" says of its Figure 2: "The line from D to E is dashed for
  reasons that will become apparent" and later "That's why the line from D to E is dashed"
  (no photons at E). Basis for the note that the dashed line is kept although photons now
  reach Detector 1.
- Stanford Encyclopedia, "The Role of Decoherence in Quantum Mechanics" (Bacciagaluppi;
  revision of 23 Jan 2025; `sep_qm-decoherence.html`, `.txt`, `.flat.txt`). Matched: "the
  pattern of detections at the screen cannot distinguish mere entanglement with some other
  systems from the actual use of those systems for detection at the slits"; "Bohr, however,
  rejected the attempt to apply the notion of quantum state to a description of the whole
  universe"; on von Neumann: "He then proves that it is always possible to define an
  interaction Hamiltonian that will correlate perfectly the eigenstates of any given
  observable of an 'observed' system with the eigenstates of some other suitable observable of
  an 'observer', leaving as an exercise for the reader to show that predictions are
  independent of where one places the boundary between the two"; "The Everett theory ... was
  originally developed in 1957".
- Stanford Encyclopedia, "Copenhagen Interpretation of Quantum Mechanics" (Faye; revision of
  31 May 2024; `sep_qm-copenhagen.*`). Matched: "An important consequence of von Neumann's
  solution to the measurement problem is that a type 1-process takes place only in the presence
  of the observer's consciousness"; "the measuring instrument may sometime be part of a type
  2-process, although it gives the same result with respect to the observed object (i)";
  "Eugene Wigner (1967) followed up on the suggestion of the mind's interaction by proposing
  that what causes a collapse of the wave function is the mind of the observer"; "Although von
  Neumann's and Wigner's positions are usually associated with the Copenhagen Interpretation,
  such views were definitely not Bohr's"; "he never had in mind the observer-induced collapse
  of the wave packet. Later he always talked about the interaction between the object and the
  measurement apparatus which was taken to be completely objective."
- Schlosshauer, Kofler and Zeilinger, "A Snapshot of Foundational Attitudes Toward Quantum
  Mechanics", arXiv:1301.1069 (`schlosshauer2013.pdf`, `.txt`). Matched: "a poll carried out
  among 33 participants of a conference on the foundations of quantum mechanics"; Question
  10(d) "Plays a distinguished physical role (e.g., wave-function collapse by consciousness):
  6%"; "Popular accounts have sometimes suggested that the Copenhagen interpretation attributes
  such a role to consciousness. In our view, this is to misunderstand the Copenhagen
  interpretation." The poll was taken in July 2011 (the paper's text; our notes on "The World:
  An Introduction" give the same year).
- Wikipedia, "Wave–particle duality relation" (raw, `wiki_duality.txt`). Matched: "D^2+ V^2\le
  1" and the attribution to Englert, Phys. Rev. Lett. 77, 2154 (1996), "Fringe Visibility and
  Which-Way Information: An Inequality".

## 3. Arithmetic

Script: `check_physics.py`, section "Distinct Configurations".

- A→B = (−1)·i = −i; A→C = (−1)·1 = −1; B→D = (−i)·i = 1; C→D = (−1)·i = −i.
- At D (from the figure: B→D deflected goes to E, straight to F; C→D straight goes to E,
  deflected to F): (1) E,No = 1·i = i; (2) F,No = 1·1 = 1; (3) E,Yes = (−i)·1 = −i;
  (4) F,Yes = (−i)·i = 1. Squared moduli 1,1,1,1, so 1/4 each; each detector 1/2. Correct.
- Without S: E = i + (−i) = 0; F = 1 + 1 = 2, squared modulus 4. Matches the previous post.
- Partial which-path (my derivation for the "comes in degrees" note): with normalized
  amplitudes, the state at the outputs is ½[(i|No⟩ − i|Yes⟩)|E⟩ + (|No⟩ + |Yes⟩)|F⟩] when S
  is fully flipped. If S's two states have real overlap g = ⟨No|Yes⟩, P(E) = ¼‖|No⟩ − |Yes⟩‖²
  = ¼(2 − 2g) = (1 − g)/2, so the fringe visibility equals g: g = 1 (no nudge) gives P(E) = 0,
  full interference; g = 0 (orthogonal states) gives 1/2, none. Values for g = 0.5 and 0.9 are
  printed by the script.

## 4. Claims about other posts

- "Joint Configurations" (previous post): the two lessons restated match its text.
- "Configurations and Amplitude": "It makes no sense to think of something that 'could have
  happened but didn't' exerting an effect on the world." Basis for "which 'Configurations and
  Amplitude' rejected".
- "Belief in the Implied Invisible" is order 229 in the manifest; this post is 236. "A few
  posts earlier in the book" is correct.
- "The World: An Introduction": our note there says the consciousness view "is usually traced
  to John von Neumann and Eugene Wigner" and quotes the SEP that such views "were definitely
  not Bohr's". My "Common Wisdom" note points back to it and adds only the Bohr quotations on
  the apparatus.
- "Collapse Postulates": my note points forward to its Heisenberg note (the post names
  Heisenberg there, not here).

## 5. Not verified

- Englert 1996 was not opened; the inequality is from Wikipedia. My note's stronger statement
  (visibility equals overlap for pure states) rests on the derivation above.
- No textbook that says consciousness determines experimental results was searched for. The
  note says only that the post names none.

## 6. Judgment calls for the editor

- Reserved words: "refutes" in the Response ("The experiment refutes the view that what
  someone knows decides the result"): the unread-sensor result meets this; it is standard and
  the SEP quotation supports it. "never" appears only inside or as paraphrase of the SEP's
  "never had in mind".
- The von Neumann note (paragraph "Though it is a little embarrassing") is the main judgment.
  I first wrote that the post's "embarrassing" was supported in von Neumann's case; on
  rereading the SEP, von Neumann's analysis itself predicts that an unread sensor or stray
  particle removes interference (predictions independent of the cut), and what he gave to
  consciousness was the type-1 process (a single outcome). So the post's clues tell against the
  imagined scientist's naive "what I can know decides" view, not against von Neumann's or
  Wigner's. The note, Response and n.b. now say this. The editor should check that I have not
  overstated von Neumann's position; the two SEP entries are the only sources.
- The clogic on "distinct so long as at least one particle ... anywhere is in a different
  position": a defender could say that configurations as points are distinct whenever any
  particle differs, which is true by definition. I framed the note as being about the post's
  next sentence, "This is experimentally demonstrable", which does need the condition.
- The interpretive clogic on "every configuration is about all the particles… everywhere"
  (Everett vs Bohr). Neutral, but the editor may judge it too close to the Joint note.
- Figure note (dashed line kept): a figure slip, kept because a reader following the previous
  post's convention would be misled. Cut if judged a nitpick.
- Pronouns: "he/his" for von Neumann (historical figure, allowed by STANDARDS 2.6).
