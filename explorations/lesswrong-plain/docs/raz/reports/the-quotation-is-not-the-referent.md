# Report: the-quotation-is-not-the-referent ("The Quotation is not the Referent", Yudkowsky, posted 2008-03-13)

## 1. The argument in three sentences (written before annotating)

Substituting equals for equals, applied inside belief reports, yields absurd results: John,
who knows the morning star is the evening star, seems forced to conclude that Mary believes
the evening star is Lucifer. The author diagnoses a type error: a belief about "the morning
star" is not the same kind of thing as the morning star, so inside belief reports the terms
should be quoted (or encoded visibly differently), and "morning star" is not equal to
"evening star" even though the planets are one. Keeping levels of quotation apart, like
keeping track of units in physics, is also what makes Tarski's truth sentences meaningful and
separates truth, which compares a belief to reality, from reality itself.

## 2. Sources checked

Local copies in `data/sources/4a_the-quotation-is-not-the-referent/`.

1. SEP, "Gottlob Frege" (https://plato.stanford.edu/entries/frege/, `sep_frege.txt`).
   Matched: "Frege is generally credited with identifying the following puzzle about
   propositional attitude reports"; "The descriptions 'the morning star' and 'the evening
   star' denote the same planet, namely Venus, but express different ways of conceiving of
   Venus and so have different senses"; "Frege proposed that when a term (name or
   description) follows a propositional attitude verb, it no longer denotes what it
   ordinarily denotes. Instead, Frege claims that in such contexts, a term denotes its
   ordinary sense"; "Frege identifies the denotation of a sentence as one of the two truth
   values"; "Frege distinguished two truth-values, The True and The False"; "the entire
   sentence ... also denotes its ordinary sense (namely, a thought)".
   Wikipedia, "Sense and reference" (raw, `wiki_sense_and_reference.txt`): "On Sense and
   Reference" ["Über Sinn und Bedeutung"], 1892; the morning star/evening star example.
2. McCarthy, "First Order Theories of Individual Concepts and Propositions"
   (http://jmc.stanford.edu/articles/concepts/concepts.pdf, `mccarthy_concepts.txt`; revised
   version dated 2000). Landing page http://jmc.stanford.edu/articles/concepts.html: "This
   paper was first published in Machine Intelligence 9 in 1979." Matched: "Admitting
   individual concepts as objects ... allows ordinary first order theories of necessity,
   knowledge, belief and wanting without modal operators or quotation marks and without the
   restrictions on substituting equals for equals that either device makes necessary."; "The
   problem identified by Frege—of suitably limiting the application of the substitutitivity of
   equals for equals—arises in artificial intelligence as well as in philosophy and
   linguistics for any system that must represent information about beliefs, knowledge,
   desires, or logical necessity" (the note elides the dash-clause with \ldots); "Mike is the
   concept of Mike; i.e. it is the sense of the expression "Mike". mike is Mike himself."
   (pdftotext splits "M ike"). The note says it quotes the revised version.
3. SEP, "Provability Logic" (https://plato.stanford.edu/entries/logic-provability/,
   `sep_provability.txt`). Matched: "If PA ⊢ A, then PA ⊢ Prov(⌜A⌝)" (first Löb condition);
   "Even though all sentences provable in Peano Arithmetic are indeed true about the natural
   numbers, Löb showed that the formalized version of this fact, Prov(⌜B⌝) → B, can be proved
   in Peano Arithmetic only in the trivial case that Peano Arithmetic already proves B
   itself."
4. SEP, "Tarski's Truth Definitions" (https://plato.stanford.edu/entries/tarski-truth/,
   `sep_tarski_truth.txt`). Matched: "Tarski escapes the paradox by using (in general)
   infinitely many sentences of M to express truth ... So the technical problem is to find a
   single formula φ that allows us to deduce all these sentences from the axioms of M";
   "Tarski's own name for this criterion of material adequacy was Convention T." I could not
   fetch Tarski's 1944 paper itself (ditext.com reset the connection).
5. "Terminal Values and Instrumental Values" (`data/originals/`, posted 2007-11-15):
   "separate and incompatible types"; "TYPE ERROR: No constructor found for Expected_Utility ->
   Utility."
6. Pointers to earlier notes: `annotated/posts/the-simple-truth.tex` (rival views accept
   Tarski's sentences, SEP deflationism) and `annotated/posts/what-is-evidence.tex`
   (Tarski's neutrality).

## 3. Arithmetic

- Encoding (a=1 ... z=26, space=0): m13 o15 r18 n14 i9 n14 g7 _0 s19 t20 a1 r18 matches
  13.15.18.14.9.14.7.0.19.20.1.18; e5 v22 e5 n14 i9 n14 g7 _0 s19 t20 a1 r18 matches
  5.22.5.14.9.14.7.0.19.20.1.18.
- (2+2)+3 = 7, 4+3 = 7. Speed of light 299,792,458 m/s (correct figure).
- Provability: if PA ⊢ P then PA ⊢ Prov(P) (Löb condition 1); if PA ⊢ Prov(P) then Prov(P)
  is true (PA proves only truths), i.e. P is provable. So the two meta-statements hold
  together for PA. For a consistent but Σ1-unsound theory (e.g. PA + ¬Con(PA)) the converse
  can fail; the note restricts itself to "the encoded system is the system itself, as for
  Peano arithmetic".

## 4. Claims about other posts

- "Terminal Values and Instrumental Values": quoted above.
- "The Simple Truth", "What Is Evidence?": pointers to existing notes only (the notes'
  content checked in the annotated files).

## 5. Not verified

- Tarski 1944 itself (see above); the note relies on the SEP entry and says so.
- The exact 1979 wording of McCarthy's sentences (only the revised version on his site was
  available); the note says it quotes the revised version.

## 6. Judgment calls

1. The Frege and McCarthy credit notes (P2, P4, P6, P7) and the Response: the post does not
   claim novelty ("usually phrased", "P'rsnally"). I present the history as information and
   the fault only as "names no one" and "does not say which proposals it disagrees with". A
   fair defender may say a blog post need not survey the literature; the reason it matters
   here is that the post itself invokes the ongoing argument ("The argument is still going
   on") and then says quote marks settle it, while quotation was one of the rival devices
   (McCarthy's own words).
2. "close to Frege's answer": Frege's senses are not quoted expressions or mental tokens, so
   "close to", not "the same". Check the wording is not stronger anywhere: note P5,
   Response, honest n.b. all say "close".
3. The provability clogic: a technical note on an illustration whose point survives. It is
   right for PA (derivation above), but it is the kind of note the editor may judge a
   nitpick. The Response mentions it in one sentence, outside "In short".
4. The Tarski note ("loosely put") is informational; the SEP itself says Tarski used
   "infinitely many sentences ... to express truth", so the post's wording is not far off.
5. Last paragraph: "states a correspondence view without argument" with a pointer to the
   earlier full treatment (STANDARDS 2.5).
6. Pronouns: Frege, McCarthy, Tarski are historical figures (he/his kept, STANDARDS 2.6).
7. Layout: a 4.6pt overfull box from the post's own encoded strings in a quote.
